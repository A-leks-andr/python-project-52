from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

menu_unregistered = [
    {"url_name": "users", "name": "Пользователи"},
    {"url_name": "login", "name": "Вход"},
    {"url_name": "create", "name": "Регистрация"},
]


class UsersView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {"menu": menu_unregistered}
        return render(request, "users/users.html", context=data)


class CreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = {"menu": menu_unregistered}
        return render(request, "users/create.html", context=data)
