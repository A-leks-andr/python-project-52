from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.menu import menu_registered
from task_manager.task.filters import TaskFilter
from task_manager.task.forms import CreateTaskForm
from task_manager.task.models import Task


class TaskListView(LoginRequiredMixin, FilterView, ListView):
    model = Task
    template_name = "task/tasks_list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_queryset(self):
        return (
            Task.objects.select_related("author", "executor", "status")
            .all()
            .order_by("id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = "task/create_task.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Создать задачу"
        context["button"] = "Создать"
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task/task.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Просмотр задачи"
        return context


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "task/delete_task.html"
    success_url = reverse_lazy("tasks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удалить задачу"
        context["button"] = "Подтвердить удаление"
        return context

    def test_func(self):
        """Проверка: текущий пользователь должен быть автором задачи."""
        task = self.get_object()
        return task.author == self.request.user  # type: ignore

    def handle_no_permission(self):
        """Что делать, если тест test_func вернул False."""
        messages.error(self.request, "Задачу может удалить только её автор")
        return redirect("tasks")

    def form_valid(self, form):
        """Сообщение об успехе при успешном удалении."""
        messages.success(self.request, "Задача успешно удалена")
        return super().form_valid(form)  # type: ignore


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = "task/create_task.html"
    success_url = reverse_lazy("tasks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Изменить задачу"
        context["button"] = "Изменить"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Задача успешно изменена.")
        return response
