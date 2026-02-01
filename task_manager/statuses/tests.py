from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.list_url = reverse("statuses")
        self.create_url = reverse("create_status")

        self.status1 = Status.objects.create(name="Активный")
        self.update_url = reverse(
            "update_status", kwargs={"pk": self.status1.pk}
        )
        self.delete_url = reverse(
            "delete_status", kwargs={"pk": self.status1.pk}
        )

    def test_status_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(response, self.status1.name)

    def test_status_create_view_post_valid_data(self):
        data = {"name": "Новый"}
        response = self.client.post(self.create_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Status.objects.filter(name="Новый").exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Статус успешно создан")

    def test_status_create_view_post_invalid_data(self):
        data = {"name": ""}
        response = self.client.post(self.create_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Status.objects.filter(name="").exists())

    def test_status_update_view_post_valid_data(self):
        data = {"name": "Обновленный"}
        response = self.client.post(self.update_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, "Обновленный")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Статус успешно изменен'
        )

    def test_status_delete_view_post_success(self):
        response = self.client.post(self.delete_url, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Status.objects.filter(pk=self.status1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Статус успешно удален'
        )
