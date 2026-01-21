from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path("", views.StatusesView.as_view(), name="statuses"),
    path("create/", views.StatusCreateView.as_view(), name="create_status"),
]
