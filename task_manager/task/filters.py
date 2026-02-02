import django_filters
from django import forms
from django.contrib.auth import get_user_model

from .models import Label, Status, Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label="Статус"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), label="Метка"
    )

    my_tasks = django_filters.BooleanFilter(
        label="Только свои задачи",
        method="filter_my_tasks",
        widget=forms.CheckboxInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.label_suffix = ""
        executor_field = self.form.fields["executor"]
        executor_field.label_from_instance = lambda obj: obj.get_full_name()  # type: ignore

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)  # type: ignore
        return queryset

    class Meta:
        model = Task
        fields = []
