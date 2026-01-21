from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self) -> str:
        return self.name
