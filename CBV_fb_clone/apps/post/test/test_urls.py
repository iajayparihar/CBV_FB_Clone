from django.test import TestCase
from post.urls import *
from post.views import *
from django.urls import reverse, resolve

class RegisterUrlTestClass(TestCase):
    def test_postUrl(self):
        # import pdb;pdb.set_trace()
        url = reverse('Post:post')
        self.assertEqual(resolve(url).func.view_class,PostFormView)