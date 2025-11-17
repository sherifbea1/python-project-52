from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from task_manager.models import Status, Task, Label


class TaskFilterTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='pass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass123'
        )

        self.status_a = Status.objects.create(name='Status A')
        self.status_b = Status.objects.create(name='Status B')

        self.task_a = Task.objects.create(
            name='Task A',
            description='Task with Status A',
            status=self.status_a,
            author=self.user
        )
        self.task_b = Task.objects.create(
            name='Task B',
            description='Task with Status B',
            status=self.status_b,
            author=self.other_user
        )

    def test_filter_by_status(self):
        self.client.login(username='tester', password='pass123')

        url = reverse('task_list') + f'?status={self.status_a.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task A')
        self.assertNotContains(response, 'Task B')

    def test_filter_by_executor(self):
        executor = User.objects.create_user(
            username='executor',
            password='pass123'
        )

        self.task_a.executor = executor
        self.task_a.save()

        self.client.login(username='tester', password='pass123')

        url = reverse('task_list') + f'?executor={executor.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task A')
        self.assertNotContains(response, 'Task B')

    def test_filter_by_label(self):
        label = Label.objects.create(name='Urgent')
        self.task_b.labels.add(label)

        self.client.login(username='tester', password='pass123')

        url = reverse('task_list') + f'?labels={label.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task B')
        self.assertNotContains(response, 'Task A')

    def test_filter_only_my_tasks(self):
        self.client.login(username='tester', password='pass123')

        url = reverse('task_list') + '?only_my=on'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task A')
        self.assertNotContains(response, 'Task B')
