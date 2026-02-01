from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.menu import menu_registered, menu_unregistered
from task_manager.users.forms import UserRegistrationForm, UserUpdateDataForm

User = get_user_model()
# Create your views here.


class UsersView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "records"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["menu"] = menu_registered
        else:
            context["menu"] = menu_unregistered
        return context


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_unregistered
        context["title"] = "Регистрация"
        context["button"] = "Зарегистрировать"
        return context

    def form_valid(self, form):
        messages.success(
            self.request, "Пользователь успешно зарегистрирован"
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateDataForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy("users")

    def test_func(self):
        user_object = self.get_object()
        return self.request.user == user_object

    def handle_no_permission(self):
        messages.error(self.request, "Вы не можете изменить чужую запись.")
        return redirect("users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Изменения пользователя"
        context["button"] = "Изменить"
        return context

    def form_valid(self, form):
        user = form.save(commit=False)

        password = form.cleaned_data.get("password_1")

        if password:
            user.set_password(password)
            messages.success(
                self.request, "Пользователь успешно изменен"
            )
        else:
            messages.success(
                self.request,
                "Данные пользователя успешно обновлены "
                "(пароль остался прежним).",
            )
        user.save()
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удаление пользователя"
        return context

    def test_func(self):
        return self.get_object().pk == self.request.user.pk

    def handle_no_permission(self):
        messages.error(self.request, "Чужую запись нельзя удалить.")
        return redirect("users")

    def get_success_url(self):
        return reverse_lazy("users")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            messages.success(
                request,
                f'Пользователь "{self.object.username}" успешно удалён.',  # type: ignore
            )

        except ProtectedError:
            messages.error(
                request,
                f'''Нельзя удалить пользователя 
                "{self.object.username}", потому что он используется.''',  # type: ignore
            )
        return redirect(self.get_success_url())
