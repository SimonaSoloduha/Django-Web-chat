from django.shortcuts import render
from django.urls import reverse

from django.views import generic
from django.views.generic import CreateView

from chat.models import Chat


def lobby(request, lobby_id):
    chat = Chat.objects.filter(id=lobby_id).first()
    #
    # old_messages = chat.messages.all()
    # chat_users = old_messages.values_list('user').distinct()
    # chat_users = list(i[0] for i in chat_users)

    # chat = Chat.objects.filter(id=lobby_id).prefetch_related('messages').first()

    old_messages = chat.messages.all()
    chat_users = old_messages.values_list('user').distinct()
    chat_users = list(i[0] for i in chat_users)

    return render(request, 'chat/lobby.html', context={'chat': chat,
                                                       'old_messages': old_messages,
                                                       'chat_users': chat_users})


class ChatListView(generic.ListView):
    model = Chat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chat_list'
    queryset = Chat.objects.order_by('-created_at')


class PostCreateView(CreateView):
    model = Chat
    template_name = 'chat/chat_list.html'
    fields = ['name', ]

    def get_context_data(self, **kwargs):
        all_chats = Chat.objects.order_by('-created_at')
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['all_chats'] = all_chats
        return context

    def get_success_url(self):
        return reverse('lobby', args=(self.object.id,))
