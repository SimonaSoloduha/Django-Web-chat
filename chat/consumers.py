from datetime import datetime

import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth.models import User

from chat.models import Message, Chat

new_messages = []
see_messages = []
new_users = []


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        global see_messages

        text_data_json = json.loads(text_data)

        try:
            if text_data_json['see_message']:

                for mes in new_messages:
                    if mes.user.id != text_data_json['auth_user_id']:
                        if mes.chat.id == text_data_json['chat']:
                            mes.message_see = True
                            mes.save()
                            new_messages.remove(mes)
                            see_messages.append(mes)

                if see_messages:
                    for mes in see_messages:
                        if mes.user.id == text_data_json['auth_user_id']:
                            self.send(text_data=json.dumps({
                                'type': 'see_messages',
                                'see_messages_id': mes.id,
                            }))
                            see_messages.remove(mes)

        except KeyError:
            message = text_data_json['message']
            chat = text_data_json['chat']
            user_name = self.scope["user"].username
            user = User.objects.filter(username=user_name).first()
            user_chat = Chat.objects.filter(id=chat).first()

            new_massage = Message.objects.create(
                user=user,
                text=message,
                chat=user_chat,
            )
            new_massage.save()

            new_massage_id = new_massage.id
            new_messages.append(new_massage)

            chat_users = text_data_json['chat_users']
            add_user = 0
            if user.id not in chat_users and user.id not in new_users:
                new_users.append(user.id)
                count_users = len(new_users) + len(chat_users)
                add_user = f'Участников: {count_users}'

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'chat': chat,
                    'sender': user_name,
                    'new_massage_id': new_massage_id,
                    'add_user': add_user,
                }
            )

    def chat_message(self, event):
        now = datetime.now()
        user_time = now.strftime("%H:%M")

        new_massage = Message.objects.filter(id=event['new_massage_id']).first()
        new_massage.message_see = False
        new_massage.save()

        self.send(text_data=json.dumps({
            'type': 'chat',
            'chat_id': new_massage.chat.id,
            'message': event['message'],
            'user_name': self.scope["user"].username,
            'user_time': user_time,
            'sender': event['sender'],
            'new_massage_id': event['new_massage_id'],
            'add_user': event['add_user'],
        }))
