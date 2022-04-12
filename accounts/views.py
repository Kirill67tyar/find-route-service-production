from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate, login, logout,
)

from accounts.forms import LoginForm, RegistrationModelForm

__all__ = (
    'login_view',
    'logout_view',
    'registration_view',
)


def login_view(request):
    form = LoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or '/'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form, })


def logout_view(request):
    logout(request)
    return redirect('/')


def registration_view(request):
    form = RegistrationModelForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        new_user = form.save(commit=False)
        new_user.set_password(password)
        new_user.save()
        return render(request, 'accounts/register_done.html', {'new_user': new_user, })
    return render(request, 'accounts/register.html', {'form': form, })
