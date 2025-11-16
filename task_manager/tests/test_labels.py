from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Label

class LabelCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')
        self.label = Label.objects.create(name='urgent')

    def test_label_list_view(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'urgent')

    def test_label_create_view(self):
        response = self.client.post(reverse('label_create'), {'name': 'bug'})
        self.assertRedirects(response, reverse('label_list'))
        self.assertTrue(Label.objects.filter(name='bug').exists())

    def test_label_update_view(self):
        response = self.client.post(reverse('label_update', args=[self.label.id]), {'name': 'critical'})
        self.assertRedirects(response, reverse('label_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'critical')

    def test_label_delete_view(self):
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        self.assertRedirects(response, reverse('label_list'))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())