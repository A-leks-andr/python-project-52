import django_filters
from django.contrib.auth import get_user_model

from .models import Label, Status, Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label="Статус"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label="Исполнитель"
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), label="Метка"
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label"]
