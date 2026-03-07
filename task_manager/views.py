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
from task_manager.utils import get_client_ip


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_ip"] = get_client_ip(self.request)

        if self.request.user.is_authenticated:
            context["menu"] = menu_registered
        else:
            context["menu"] = menu_unregistered
        return context


class UserLoginView(View):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def get_common_context(self, form):
        return {
            "menu": menu_unregistered,
            "form": form,
            "user_ip": get_client_ip(self.request),
        }

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(
            request, self.template_name, self.get_common_context(form)
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            # username = form.cleaned_data.get("username")

            user = form.get_user()
            login(request, user)
            # messages.success(request, f"Добро пожаловать, {username}!")
            messages.success(request, "Вы залогинены")

            return redirect(self.success_url)
        else:
            messages.error(
                request,
                "Имя пользователя или пароль неверны. "
                "Пожалуйста, попробуйте еще раз.",
            )

            return render(
                request, self.template_name, self.get_common_context(form)
            )


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        # username = request.user.username
        # messages.success(request, f"Вы вышли {username}")
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
