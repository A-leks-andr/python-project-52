from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.task.models import Task


class LabelCRUDTests(TestCase):
    def setUp(self):
        # Создаем пользователя, так как LoginRequiredMixin требует авторизации
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        # Создаем статус для тестов с задачами
        self.status_new = Status.objects.create(name="Новый")

        self.client = Client()
        # Авторизуем клиента сразу для всех тестов
        self.client.force_login(self.user)

        self.list_url = reverse("labels")
        self.create_url = reverse("create_label")

        self.label1 = Label.objects.create(name="Активный")
        self.update_url = reverse("update_label", kwargs={"pk": self.label1.pk})
        self.delete_url = reverse("delete_label", kwargs={"pk": self.label1.pk})

    def test_label_list_view(self):
        """Проверка списка меток."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, self.label1.name)

    def test_label_create_view_post_valid_data(self):
        """Создание новой метки."""
        data = {"name": "Срочно"}
        response = self.client.post(self.create_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name="Срочно").exists())
        self.assertContains(
            response, f"Метка &quot;{data['name']}&quot; успешно создана."
        )

    def test_label_create_view_post_invalid_data(self):
        """Попытка создания пустой метки."""
        data = {"name": ""}
        response = self.client.post(self.create_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(name="").exists())

    def test_label_update_view_post_valid_data(self):
        """Изменение метки (разрешено всегда)."""
        data = {"name": "Обновленный"}
        response = self.client.post(self.update_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "Обновленный")
        # Проверка сообщения через "е"
        self.assertContains(
            response, f"Метка &quot;{data['name']}&quot; успешно изменена."
        )

    def test_label_delete_view_post_success(self):
        """Успешное удаление свободной метки."""
        # Убеждаемся, что метка не привязана к задачам
        self.label1.tasks_with_label.clear()  # type: ignore
        response = self.client.post(self.delete_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=self.label1.pk).exists())
        self.assertContains(
            response, f"Метка &quot;{self.label1.name}&quot; успешно удалена."
        )

    def test_label_delete_view_used_in_task(self):
        """Запрет на удаление метки, если она привязана к задаче."""
        # Создаем задачу и привязываем метку
        task = Task.objects.create(
            name="Test Task", author=self.user, status=self.status_new
        )
        task.label.add(self.label1)

        # Пытаемся удалить
        response = self.client.post(self.delete_url, follow=True)

        # Метка ДОЛЖНА остаться в базе
        self.assertTrue(Label.objects.filter(pk=self.label1.pk).exists())

        # Проверяем сообщение об ошибке (должно в точности совпадать с View)
        self.assertContains(response, "Нельзя удалить используемую метку")
        self.assertContains(response, "так как она привязана к задачам")
        self.assertContains(response, self.label1.name)
