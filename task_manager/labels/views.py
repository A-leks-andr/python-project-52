from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_queryset(self):
        return Label.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        return context


class LabelCreateView(CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.label_suffix = ""  # Убирает ":" после слова "Имя"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Создать метку"
        context["button"] = "Создать"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Метка успешно создана"
            # f'Метка "{self.object.name}" успешно создана.',  # type:ignore
        )
        return response


class LabelUpdateView(UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.label_suffix = ""  # Убирает ":" после слова "Имя"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Изменить метку"
        context["button"] = "Изменить"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Метка успешно изменена"
            #f'Метка "{self.object.name}" успешно изменена.',  # type:ignore
        )
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete_label.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удалить метку"
        context["button"] = "Да, удалить"
        return context

    def get_success_url(self):
        return reverse_lazy("labels")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks_with_label.exists():  # type: ignore
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
               # f'''Нельзя удалить используемую метку 
               # "{self.object.name}", так как она привязана к задачам.''',  
               # type: ignore
            )
            return redirect(self.get_success_url())

        messages.success(
            self.request, "Метка успешно удалена"
            # f'Метка "{self.object.name}" успешно удалена.',  # type: ignore
        )
        return super().post(request, *args, **kwargs)
