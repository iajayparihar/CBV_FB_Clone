from register.serializers import RegisterSerializer
from register.models import CustomUser
from django.test import TestCase
from django.urls import reverse

class RegisterSerializerTestCase(TestCase):
        def setUp(self):
            self.url = reverse('Register:register')
            self.data = {
                'username': 'testuser',
                'password': 'testpassword',
                'email': 'test@example.com',
                'mobile': '1234567890',
                'DOB': '2000-01-01',
                'gender': 'Male'
            }            
        
        def test_Register_with_serializer(self):
            user = CustomUser.objects.create(username='testuser',\
                                            password='testpassword',\
                                            email='test@example.com',\
                                            mobile='1234567890',\
                                            DOB='2000-01-01',\
                                            gender='Male',) 
            serializer = RegisterSerializer(user)

            self.assertEqual(serializer.data.get('username'), self.data.get('username'))