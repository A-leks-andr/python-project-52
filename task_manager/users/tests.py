from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.statuses.models import Status

User = get_user_model()  # доступ к модели


class UserModelTests(TestCase):
    """
    Набор тестов для стандартной модели пользователя Django
    (с использованием username, first_name, last_name и date_joined).
    """

    def test_create_user_with_username(self):
        """
        Проверка успешного создания обычного пользователя.
        """
        user = User.objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            password="securepassword123",
        )
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.is_active)

        self.assertIsNotNone(user.date_joined)
        self.assertLess(user.date_joined, timezone.now())

    def test_update_user_details(self):
        """
        Проверка изменения полей пользователя (first_name, last_name).
        """
        user = User.objects.create_user(
            username="testuser", password="password123"
        )

        new_first_name = "Jane"
        new_last_name = "Smith"

        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()

        updated_user = User.objects.get(username="testuser")
        self.assertEqual(updated_user.first_name, new_first_name)
        self.assertEqual(updated_user.last_name, new_last_name)

    def test_delete_user(self):
        """
        Проверка удаления пользователя из системы.
        """
        user = User.objects.create_user(
            username="user_to_delete", password="password123"
        )
        self.assertEqual(User.objects.count(), 1)

        user.delete()

        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="user_to_delete")

    # Тест на уникальность username
    def test_create_user_duplicate_username(self):
        """
        Проверка уникальности username.

        """
        User.objects.create_user(username="uniqueuser", password="foo")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="uniqueuser", password="bar")


class UserViewsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="pass1"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="pass2"
        )
        self.status1 = Status.objects.create(name="New")
        self.update_url = reverse("update", kwargs={"pk": self.user1.pk})
        self.delete_url = reverse("delete", kwargs={"pk": self.user1.pk})

    # 1. Закрываем строки 73-86 (UserUpdateView: попытка изменить чужой профиль)
    def test_update_another_user_permission(self):
        self.client.login(username="user2", password="pass2")
        response = self.client.get(
            reverse("update", kwargs={"pk": self.user1.pk})
        )

        # Проверяем редирект и наличие сообщения об ошибке
        self.assertRedirects(response, reverse("users"))
        messages = list(response.wsgi_request._messages)  # type: ignore
        self.assertEqual(
            str(messages[0]),
            "У вас нет прав для изменения другого пользователя.",
        )

    # 2. Закрываем логику смены пароля в UserUpdateView
    def test_user_update_with_password(self):
        # 1. Логинимся под пользователем, которого хотим изменить
        self.client.login(username="user1", password="pass1")

        # 2. Подготавливаем данные (все поля формы теперь обязательны)
        data = {
            "username": "user1_new",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "password1": "new_pass123",  # Имя поля как в вашей форме
            "password2": "new_pass123",  # Обязательный повтор
        }

        # 3. Отправляем запрос
        response = self.client.post(self.update_url, data)

        # 4. ПРОВЕРКИ
        # Ожидаем редирект (302), что значит форма валидна и сохранена
        self.assertEqual(response.status_code, 302)

        # Обновляем данные объекта из базы
        self.user1.refresh_from_db()

        # Проверяем, что имя изменилось
        self.assertEqual(self.user1.username, "user1_new")
        # Проверяем, что новый пароль установился корректно
        self.assertTrue(self.user1.check_password("new_pass123"))

        # Проверяем наличие flash-сообщения (опционально, но круто для покрытия)
        messages = list(response.wsgi_request._messages)  # type: ignore
        self.assertEqual(str(messages[0]), "Пользователь успешно изменен")
