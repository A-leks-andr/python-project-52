from django.urls import path

from task_manager.task import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
]
