from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.menu import menu_registered
from task_manager.statuses.models import Status


class StatusesView(ListView):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        return context


class StatusCreateView(CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create_status.html"
    success_url = reverse_lazy("statuses")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.label_suffix = ""  # Убирает ":" после слова "Имя"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Создать статус"
        context["button"] = "Создать"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Статус успешно создан"
            # f"Статус '{self.object.name}' успешно создан.",  # type:ignore
        )
        return response


class StatusUpdateView(UpdateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create_status.html"
    success_url = reverse_lazy("statuses")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Изменить статус"
        context["button"] = "Сохранить изменения"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Статус "{self.object.name}" успешно изменён.',  # type:ignore
        )
        return response


class StatusDeleteView(DeleteView):
    model = Status
    template_name = "statuses/delete_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удалить статус"
        context["button"] = "Подтвердить удаление"
        return context

    def get_success_url(self):
        return reverse_lazy("statuses")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)  # type:ignore
            messages.success(
                self.request,
                f'Статус "{self.object.name}" успешно удалён.',  # type:ignore
            )
            return response

        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить используемый статус '{self.object.name}'",  # type:ignore
            )
            return redirect(self.get_success_url())
