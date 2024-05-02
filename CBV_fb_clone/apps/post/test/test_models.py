import pytest
from django.contrib.auth import get_user_model
from post.models import UserPost, Like, UserComments

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='test_user', email='test@example.com', password='password')

@pytest.fixture
def user_post(user):
    return UserPost.objects.create(user=user, image='test_image.jpg', location='Test Location', cap='Test Caption', desc='Test Description')

@pytest.fixture
def like(user, user_post):
    return Like.objects.create(user=user, post=user_post)

@pytest.fixture
def user_comment(user, user_post):
    return UserComments.objects.create(user=user, post=user_post, comment='Test Comment')


@pytest.mark.django_db
def test_user_post_creation(user_post):
    assert UserPost.objects.count() == 1
    assert UserPost.objects.first().user.username == 'test_user'

@pytest.mark.django_db
def test_like_creation(like):
    assert Like.objects.count() == 1
    assert Like.objects.first().user.username == 'test_user'

@pytest.mark.django_db
def test_user_comment_creation(user_comment):
    assert UserComments.objects.count() == 1
    assert UserComments.objects.first().user.username == 'test_user'
