from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory


class LoginViewTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertTrue('Kaaster' in response.content)
        self.assertTrue(200 == response.status_code)

    def test_login_redirect_to_index(self):
    	self.user = User.objects.create_user(
            username='razvan', email='razvan@a.com', password='parola123')
        response = self.client.post(reverse('login'), {'username': 'razvan', 'password': 'parola123'})
        self.assertRedirects(response, reverse('index'))

    def test_register_redirect_to_index(self):
        response = self.client.post(reverse('register'), {'username': 'razvan', 'password': 'parola123', 'email': 'aaa@a.com'})
        self.assertRedirects(response, '/user_profile/razvan/')
