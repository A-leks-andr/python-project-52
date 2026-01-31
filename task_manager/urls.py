from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("users/", include("task_manager.users.urls")),
    path("admin/", admin.site.urls),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("statuses/", include("task_manager.statuses.urls")),
    path("labels/", include("task_manager.labels.urls")),
    path("tasks/", include("task_manager.task.urls")),
    path("rollbar_test/", views.rollbar_test, name='rollbar_test')
]
