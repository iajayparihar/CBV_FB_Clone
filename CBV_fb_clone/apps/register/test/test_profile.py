from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
class ProfileViewTest(TestCase):
    def setUp(self):
        self.url = reverse('Register:profile')
        self.dashboard_template = 'post/dashboard.html'

    def test_profile_view_redirects_if_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_profile_view_renders_dashboard_if_authenticated(self):
        # Create a custom user and login
        username = 'testuser'
        password = 'testpassword'
        obj = get_user_model()
        obj.objects.create_user(username=username, password=password)

        self.client.login(username=username, password=password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)