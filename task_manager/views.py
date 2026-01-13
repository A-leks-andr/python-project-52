from django.shortcuts import render
from django.views.generic import TemplateView

menu_unregistered = [
    {'url_name': 'users', 'name': 'Пользователи'},
    {'url_name': 'login', 'name': 'Вход'},
    {'url_name': 'create', 'name': 'Регистрация'},
]

class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {'menu': menu_unregistered}
        return render(request, "index.html", context=data)


class UsersView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {'menu': menu_unregistered}
        return render(request, "users.html", context=data)

class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {'menu': menu_unregistered}
        return render(request, "login.html", context=data)


class CreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {'menu': menu_unregistered}
        return render(request, "create.html", context=data)
