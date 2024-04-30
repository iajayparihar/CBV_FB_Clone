from django.test import TestCase
from post.models import *
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

User = get_user_model()
class PostModelTestCase(TestCase):
    def setUp(self) -> None:
        self.url = reverse('Post:post')  
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        return super().setUp()

    def test_postModel(self):
        UserPost.objects.create(user=self.user, image=\
        SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),\
        location = "in test case", cap = 'abc', desc = 'desc test case')

        obj = UserPost.objects.get(user=self.user)
        self.assertIsInstance(obj,UserPost)