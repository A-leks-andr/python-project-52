from django.contrib import messages
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from task_manager.menu import menu_registered
from task_manager.statuses.models import Status


class StatusesView(ListView):
    model = Status
    template_name = "statuses/statuses.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        return context


class StatusCreateView(CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Создать статус"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Статус '{self.object.name} успешно создан.",  # type:ignore
        )
        return response
