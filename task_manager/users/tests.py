from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

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
        # Проверка, что стандартное поле 'date_joined'
        # было автоматически заполнено
        self.assertIsNotNone(user.date_joined)
        self.assertLess(user.date_joined, timezone.now())
        # Убедимся, что дата в прошлом или сейчас

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
