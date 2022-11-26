from django.urls import path

from app_users.views import Logout, Login, register_user_view

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', register_user_view, name='register'),
]
