from post.serializers import PostSerializer
from post.models import UserPost
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
User = get_user_model()
class PostSerializerTestClass(TestCase):
    def setUp(self) -> None:
        self.url = reverse('Post:post')  
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        return super().setUp()
    def test_post_with_serializer(self):
        post = UserPost.objects.create(user= self.user,
            image =  SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            location = "in test case",
            cap = 'This is a test post content.',
            desc =  "test description",
        )
        serializer = PostSerializer(post)
        self.assertEqual(serializer.data.get('desc'), "test description")   