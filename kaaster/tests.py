from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class LoginViewTests(TestCase):
    def test_index_redirects_to_login(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login')

    def test_login_successful(self):
        User.objects.create_user(username='razvan', password='parola123')
        response = self.client.post(reverse('login'),
                                    {'username': 'razvan',
                                     'password': 'parola123'})
        self.assertRedirects(response, '/')
