from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Status, Task


class TaskCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.other_user = User.objects.create_user(
            username='user2',
            password='pass123'
        )

        self.status = Status.objects.create(name='In progress')

        self.task = Task.objects.create(
            name='Test task',
            description='Some description',
            status=self.status,
            author=self.user,
            executor=self.other_user
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, '/login/?next=/tasks/')

    def test_list_tasks_logged_in(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task')

    def test_view_task_detail(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_create_task(self):
        self.client.login(username='user1', password='pass123')
        data = {
            'name': 'New task',
            'description': 'Test description',
            'status': self.status.id,
            'executor': self.other_user.id
        }
        response = self.client.post(
            reverse('task_create'),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name='New task').exists())
        self.assertContains(response, 'Task created successfully')

    def test_update_task(self):
        self.client.login(username='user1', password='pass123')
        data = {
            'name': 'Updated task',
            'description': 'Updated description',
            'status': self.status.id,
            'executor': self.other_user.id
        }
        response = self.client.post(
            reverse('task_update', args=[self.task.id]),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated task')
        self.assertContains(response, 'Task updated successfully')

    def test_delete_task_by_author(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('task_delete', args=[self.task.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        self.assertContains(response, 'Task deleted successfully')

    def test_delete_task_by_not_author(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('task_delete', args=[self.task.id]),
            follow=True
        )
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        self.assertContains(response, "You cannot delete someone else")