from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.models import Label


class LabelCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.list_url = reverse("labels")
        self.create_url = reverse("create_label")

        self.label1 = Label.objects.create(name="Активный")
        self.update_url = reverse("update_label", kwargs={"pk": self.label1.pk})
        self.delete_url = reverse("delete_label", kwargs={"pk": self.label1.pk})

    def test_label_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, self.label1.name)

    def test_label_create_view_post_valid_data(self):
        data = {"name": "Новый"}
        response = self.client.post(self.create_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Label.objects.filter(name="Новый").exists())
        new_label = Label.objects.get(name="Новый")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Метка "{new_label.name}" успешно создана.'
        )

    def test_label_create_view_post_invalid_data(self):
        data = {"name": ""}
        response = self.client.post(self.create_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Label.objects.filter(name="").exists())

    def test_label_update_view_post_valid_data(self):
        data = {"name": "Обновленный"}
        response = self.client.post(self.update_url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "Обновленный")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Метка "{self.label1.name}" успешно изменёна.'
        )

    def test_label_delete_view_post_success(self):
        response = self.client.post(self.delete_url, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Label.objects.filter(pk=self.label1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Метка "{self.label1.name}" успешно удалёна.'
        )
