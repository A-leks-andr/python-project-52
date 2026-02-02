from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Label, Status, Task

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        # 1. Создаем тестовых пользователей
        self.user_author = User.objects.create_user(
            username="author_user",
            password="testpassword123",
            first_name="Ivan",
            last_name="Smit",
        )
        self.user_executor = User.objects.create_user(
            username="executor_user",
            password="testpassword123",
            first_name="Igor",
            last_name="Braun",
        )
        self.user_another = User.objects.create_user(
            username="another_user",
            password="testpassword123",
            first_name="David",
            last_name="Boy",
        )

        # 2. Создаем необходимые Status и Label
        self.status_new = Status.objects.create(name="Новый")
        self.status_in_progress = Status.objects.create(name="В работе")
        self.label_critical = Label.objects.create(name="Критическая")

        # 3. Создаем базовую задачу для тестирования Update/Delete/Detail
        self.task = Task.objects.create(
            name="Тестовая задача 1",
            description="Описание тестовой задачи",
            author=self.user_author,
            executor=self.user_executor,
            status=self.status_new,
        )
        self.task.label.add(self.label_critical)
        self.task_url_detail = reverse("task_view", kwargs={"pk": self.task.pk})
        self.task_url_update = reverse(
            "task_update", kwargs={"pk": self.task.pk}
        )
        self.task_url_delete = reverse(
            "task_delete", kwargs={"pk": self.task.pk}
        )
        self.tasks_list_url = reverse("tasks")
        self.task_create_url = reverse("task_create")

    # --- READ Tests ---

    def test_task_list_view_authenticated(self):
        """Авторизованный пользователь видит список задач."""
        self.client.force_login(self.user_another)
        response = self.client.get(self.tasks_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.get_author_name())

    def test_task_list_view_unauthenticated(self):
        """Неавторизованный пользователь перенаправляется на страницу входа."""
        response = self.client.get(self.tasks_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login") + "?next=" + self.tasks_list_url
        )

    def test_task_detail_view(self):
        """Просмотр деталей задачи."""
        self.client.force_login(self.user_another)
        response = self.client.get(self.task_url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.get_author_name())

    # --- CREATE Tests ---

    def test_create_task_valid_data(self):
        """Создание задачи с валидными данными."""
        self.client.force_login(self.user_another)

        # Данные для POST-запроса
        form_data = {
            "name": "Новая тестовая задача 2",
            "description": "Описание новой задачи",
            "executor": self.user_executor.id,  # type: ignore
            "status": self.status_in_progress.id,  # type: ignore
            "label": [self.label_critical.id],  # type: ignore
        }

        response = self.client.post(
            self.task_create_url, form_data, follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Task.objects.filter(name="Новая тестовая задача 2").exists()
        )
        new_task = Task.objects.get(name="Новая тестовая задача 2")
        self.assertEqual(new_task.author, self.user_another)

    # --- UPDATE Tests ---

    def test_update_task_view(self):
        """Обновление существующей задачи."""
        self.client.force_login(self.user_another)

        # Данные для POST-запроса (меняем статус и имя)
        updated_data = {
            "name": "Обновленное имя задачи",
            "description": self.task.description,
            "executor": self.user_executor.id,  # type: ignore
            "status": self.status_in_progress.id,  # type: ignore
            "label": [self.label_critical.id],  # type: ignore
        }

        response = self.client.post(
            self.task_url_update, updated_data, follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Обновленное имя задачи")
        self.assertEqual(self.task.status, self.status_in_progress)

    # --- DELETE Tests ---

    def test_delete_task_by_author(self):
        """Удаление задачи её автором (должно пройти)."""
        # Логиним автора задачи
        self.client.force_login(self.user_author)
        response = self.client.post(self.task_url_delete, follow=True)

        # Проверяем редирект и отсутствие задачи
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertContains(response, "Задача успешно удалена")

    def test_delete_task_by_non_author(self):
        """Попытка удаления задачи не автором (должна провалиться)."""
        # Логиним другого пользователя
        self.client.force_login(self.user_another)
        response = self.client.post(self.task_url_delete, follow=True)

        # Задача ДОЛЖНА остаться в базе
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        # Проверяем наличие ошибки
        self.assertContains(response, "Задачу может удалить только ее автор")

    def test_filter_by_status(self):
        """Проверка фильтрации по статусу."""
        self.client.force_login(self.user_author)
        # Создаем еще одну задачу с другим статусом
        Task.objects.create(
            name="Другая задача",
            author=self.user_author,
            status=self.status_in_progress,  # Статус 'В работе'
        )

        # Фильтруем по статусу 'Новый' (id из setUp)
        url = f"{self.tasks_list_url}?status={self.status_new.id}"  # type: ignore
        response = self.client.get(url)

        self.assertContains(response, self.task.name)
        self.assertNotContains(response, "Другая задача")

    def test_filter_my_tasks_checkbox(self):
        """Проверка чекбокса 'Только мои задачи'."""
        # Создаем задачу, где автором является другой пользователь
        Task.objects.create(
            name="Чужая задача",
            author=self.user_another,
            status=self.status_new,
        )

        # Логинимся под автором первой задачи
        self.client.force_login(self.user_author)

        # 1. Без чекбокса видим обе задачи
        response_all = self.client.get(self.tasks_list_url)
        self.assertContains(response_all, self.task.name)
        self.assertContains(response_all, "Чужая задача")

        # 2. С чекбоксом видим только свою
        response_filtered = self.client.get(
            f"{self.tasks_list_url}?my_tasks=on"
        )
        self.assertContains(response_filtered, self.task.name)
        self.assertNotContains(response_filtered, "Чужая задача")
