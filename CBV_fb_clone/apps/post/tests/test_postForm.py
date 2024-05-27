from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from post.models import UserPost
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
class PostFormViewTest(TestCase):
    def setUp(self):
        self.url = reverse('Post:post')  
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_post_form_submission(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Prepare form data
        form_data = {
            # You may need to adjust the file path to an existing file on your system
            'image': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),

            'location' : "in test case",
            'cap': 'This is a test post content.',
            'desc' : "test description",
        }

        # Submit the form
        response = self.client.post(self.url, form_data)

        #form submission was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
