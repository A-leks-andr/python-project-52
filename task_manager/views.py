from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from task_manager.forms import LoginForm
from task_manager.menu import menu_registered, menu_unregistered


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["menu"] = menu_registered
        else:
            context["menu"] = menu_unregistered
        return context


class UserLoginView(View):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        data = {"menu": menu_unregistered, "form": form}

        return render(request, self.template_name, context=data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")

            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {username}!")

            return redirect(self.success_url)
        else:
            messages.error(
                request,
                "Имя пользователя или пароль неверны. "
                "Пожалуйста, попробуйте еще раз.",
            )

            data = {"menu": menu_unregistered, "form": form}

            return render(request, self.template_name, context=data)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        messages.success(request, f"Вы вышли {username}")
        return super().dispatch(request, *args, **kwargs)
