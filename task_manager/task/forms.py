from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.task.models import Task

User = get_user_model()


class CreateTaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        to_field_name="id",
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
    )

    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метка",
        widget=forms.SelectMultiple(attrs={"size": 4, "class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "label"]
