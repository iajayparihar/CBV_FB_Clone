from django.test import TestCase
from register.models import CustomUser

class CustomUserTestCaseClass(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@example.com',
            mobile = '1234567890',
            DOB =  '2000-01-01',
            gender = 'Male'
        )
        # return super().setUp()
    def test_model_fields(self):
        user = CustomUser.objects.get(username='testuser')
        self.assertIsInstance(user,CustomUser)