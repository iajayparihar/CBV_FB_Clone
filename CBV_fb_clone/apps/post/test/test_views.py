from django.test import TestCase
from django.urls import reverse
from post.views import all_user_post
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()

class TestAllUserPostView(TestCase):
    def test_all_user_post_view_authenticated(self):
        response = self.client.get(reverse('Post:all_user_post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostFormTestCase(TestCase):
    def setUp(self):
        self.url = reverse('Post:post')  
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_post_form_submission(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'image': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),

            'location' : "in test case",
            'cap': 'This is a test post content.',
            'desc' : "test description",
        }

        # Submit the form
        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

class ViewPostTestCase(TestCase):
    def setUp(self):
        self.url = reverse('Post:post')  
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_View_Post_TC(self):     
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)