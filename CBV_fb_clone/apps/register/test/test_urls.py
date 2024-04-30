from django.test import SimpleTestCase
from register.urls import *
from register.views import *
from django.urls import reverse , resolve
class RegisterUrlTestClass(SimpleTestCase):
    def test_RegisterUrl(self):
        url = reverse('Register:register')
        self.assertEqual(resolve(url).func.view_class, register)

    def test_ProfileUrl(self):
        url = reverse("Register:profile")
        self.assertEqual(resolve(url).func.view_class, profile)