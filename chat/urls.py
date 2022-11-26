from django.urls import path

from chat.views import lobby, PostCreateView

urlpatterns = [
    path('<int:lobby_id>/', lobby, name='lobby'),
    path('', PostCreateView.as_view(), name='chats')
]
