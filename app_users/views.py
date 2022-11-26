from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from app_users.forms import RegisterForm


class Login(LoginView):
    template_name = 'users/login.html'


class Logout(LogoutView):
    next_page = '/'


def register_user_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/chats/')

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
