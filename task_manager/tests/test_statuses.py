from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Status


class StatusCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        self.status = Status.objects.create(name='In progress')

    def test_status_list_view_requires_login(self):
        """Проверяем, что неавторизованный пользователь перенаправляется"""
        self.client.logout()
        response = self.client.get(reverse('status_list'))
        self.assertRedirects(response, '/login/?next=/statuses/')

    def test_status_list_view_authenticated(self):
        """Проверяем, что авторизованный видит список статусов"""
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'In progress')

    def test_create_status(self):
        """Создание нового статуса"""
        response = self.client.post(reverse('status_create'), {'name': 'New status'}, follow=True)
        self.assertRedirects(response, reverse('status_list'))
        self.assertTrue(Status.objects.filter(name='New status').exists())

    def test_update_status(self):
        """Обновление статуса"""
        response = self.client.post(
            reverse('status_update', args=[self.status.id]),
            {'name': 'Updated status'},
            follow=True
        )
        self.assertRedirects(response, reverse('status_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated status')

    def test_delete_status(self):
        """Удаление статуса"""
        response = self.client.post(reverse('status_delete', args=[self.status.id]), follow=True)
        self.assertRedirects(response, reverse('status_list'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_cannot_delete_status_linked_to_task(self):
        """Статус нельзя удалить, если связан с задачей (пока заглушка)"""

        pass
