from django.contrib import admin
from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("users/", views.UsersView.as_view(), name="users"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("admin/", admin.site.urls),
]
