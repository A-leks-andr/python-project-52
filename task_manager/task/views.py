from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.menu import menu_registered
from task_manager.task.filters import TaskFilter
from task_manager.task.forms import CreateTaskForm
from task_manager.task.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task/tasks_list.html"
    context_object_name = "tasks"
    ordering = ["id"]

    def get_queryset(self):
        queryset = Task.objects.all().annotate(
            author_full_name=Concat(
                "author__first_name",
                Value(" "),
                "author__last_name",
                output_field=CharField(),
            ),
            executor_full_name=Concat(
                "executor__first_name",
                Value(" "),
                "executor__last_name",
                output_field=CharField(),
            ),
        )

        self.filter_set = TaskFilter(self.request.GET, queryset=queryset)

        if self.request.GET.get("my_tasks"):
            queryset = queryset.filter(author=self.request.user)
            self.filter_set = TaskFilter(self.request.GET, queryset=queryset)

        return self.filter_set.qs.distinct().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["filter"] = self.filter_set
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

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .annotate(
                author_full_name=Concat(
                    "author__first_name",
                    Value(" "),
                    "author__last_name",
                    output_field=CharField(),
                ),
                executor_full_name=Concat(
                    "executor__first_name",
                    Value(" "),
                    "executor__last_name",
                    output_field=CharField(),
                ),
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Просмотр задачи"
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task/delete_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context["title"] = "Удалить задачу"
        context["button"] = "Подтвердить удаление"
        return context

    def get_success_url(self):
        return reverse_lazy("tasks")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:  # type: ignore
            messages.error(request, "Нельзя удалить чужую задачу")
            return redirect(self.get_success_url())

        messages.success(self.request, "Задача успешно удалена")
        return super().post(request, *args, **kwargs)


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