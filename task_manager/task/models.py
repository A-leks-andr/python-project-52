from django.contrib.auth import get_user_model
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя", unique=True)
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name="Автор",
        editable=False,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        verbose_name="Исполнитель",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name="Статус"
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name="Метки",
        blank=True,
        related_name="tasks_with_label",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name

    def get_author_name(self):
        full_name = self.author.get_full_name()
        return full_name if full_name else self.author.username

    def get_executor_name(self):
        if not self.executor:
            return ""
        full_name = self.executor.get_full_name()
        return full_name if full_name else self.executor.username
