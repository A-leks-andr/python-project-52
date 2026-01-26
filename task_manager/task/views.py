from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from .models import Task
from task_manager.task.filters import TaskFilter
from task_manager.menu import menu_registered

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all().annotate(
            author_full_name=Concat(
                'author__first_name', Value(' '), 'author__last_name',
                output_field=CharField()
            ),
            executor_full_name=Concat(
                'executor__first_name', Value(' '), 'executor__last_name',
                output_field=CharField()
            )
        )
        
        self.filter_set = TaskFilter(self.request.GET, queryset=queryset)
        
        if self.request.GET.get('my_tasks'):
            queryset = queryset.filter(author=self.request.user)
            self.filter_set = TaskFilter(self.request.GET, queryset=queryset)
            
        return self.filter_set.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu_registered
        context['filter'] = self.filter_set
        return context
