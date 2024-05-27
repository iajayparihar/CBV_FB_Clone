from django.test import TestCase
from django.urls import reverse
from register.models import CustomUser

class RegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse('Register:register')
        self.data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'mobile': '1234567890',
            'DOB': '2000-01-01',
            'gender': 'Male'
        }

    def test_register_view(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)  # 302 is the status code for redirect
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
