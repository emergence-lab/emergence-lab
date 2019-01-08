from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.conf import settings

from users.urls import urlpatterns


class TestUserAppViews(TestCase):

    def setUp(self):
        self.user_obj = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_profile_view(self):
        """
        Tests user profile view
        """
        url = reverse('users_profile', kwargs={'username': self.user_obj.username})
        match = resolve('/accounts/users/detail/{}'.format(self.user_obj.username))
        response = self.client.get(url)
        self.assertEqual(match.url_name, 'users_profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_view.html')
