from django.forms import forms

from chat.models import Chat


class ChatForm(forms.Form):
    class Meta:
        model = Chat
        fields = ('name',)
