from django.urls import path

from task_manager.task import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    path(
        "<int:pk>/task_view/", views.TaskDetailView.as_view(), name="task_view"
    ),
    path(
        "<int:pk>/delete_task/",
        views.TaskDeleteView.as_view(),
        name="delete_task",
    ),
]
