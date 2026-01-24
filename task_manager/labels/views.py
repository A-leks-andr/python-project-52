from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.models import Label
from task_manager.menu import menu_registered


class LabelsView(ListView):
    model = Label
    template_name = "labels/labels_list.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        return context


class LabelCreateView(CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Создать метку"
        context["button"] = "Сохранить метку"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Метка "{self.object.name}" успешно создана.',  # type:ignore
        )
        return response


class LabelUpdateView(UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Изменить метку"
        context["button"] = "Сохранить изменения"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Метка "{self.object.name}" успешно изменёна.',  # type:ignore
        )
        return response


class LabelDeleteView(DeleteView):
    model = Label
    template_name = "labels/delete_label.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удалить метку"
        context["button"] = "Подтвердить удаление"
        return context

    def get_success_url(self):
        return reverse_lazy("labels")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)  # type:ignore
            messages.success(
                self.request,
                f'Метка "{self.object.name}" успешно удалёна.',  # type:ignore
            )
            return response

        except ProtectedError:
            messages.error(
                self.request,
                f'Нельзя удалить используемую метку "{self.object.name}"',  # type:ignore
            )
            return redirect(self.get_success_url())
