import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from post.models import UserPost, Like, UserComments

from django.test.client import Client

User = get_user_model()
client = Client()
@pytest.fixture
def user():
    return User.objects.create_user(username='test_user', email='test@example.com', password='password')

@pytest.fixture
def user_post(user):
    return UserPost.objects.create(user=user, image='test_image.jpg', location='Test Location', cap='Test Caption', desc='Test Description')

# post page rendering succes
@pytest.mark.django_db
def test_post_form_view(user):
    url = reverse('Post:post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

# post page making a post
@pytest.mark.django_db
def test_post_form_submission(user):
    client.force_login(user)
    url = reverse('Post:post')
    data = {
        'image': 'test_image.jpg',
        'location': 'Test Location',
        'cap': 'Test Caption',
        'desc': 'Test Description',
        # 'like' : 1
    }
    response = client.post(url, data,format='multipart')
    assert response.status_code == 200

# post like and unlike
@pytest.mark.django_db
def test_like_view(user, user_post):
    client.force_login(user)
    url = reverse('Post:like', kwargs={'pk': user_post.pk})
    response = client.get(url)
    assert response.status_code == 200

# comment on post
@pytest.mark.django_db
def test_comment_on_post_view(user, user_post):
    url = reverse('Post:comment_on_post', kwargs={'pk': user_post.pk})
    client.force_login(user)
    data = {'comment': 'Test comment'}
    response = client.post(url, data)
    assert response.status_code == 200

# view post
@pytest.mark.django_db
def test_view_post(user):
    url = reverse('Post:view_post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

# all user's post 
@pytest.mark.django_db
def test_all_user_post_show(user):
    url = reverse('Post:all_user_post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

# update post get method
@pytest.mark.django_db
def test_update_post_get(user,user_post):
    url = reverse('Post:update_post',kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


# update post POST method
@pytest.mark.django_db
def test_update_post_post(user,user_post):
    
    url = reverse('Post:update_post',kwargs={'pk': user_post.pk})
    client.force_login(user)
    data = {
        'image': 'test_image2.jpg',
        'location': 'Test Location thoughtwin',
        'cap': 'Test Caption2',
        'desc': 'Test Description2',}
    response = client.post(url,data=data,format='multipart')
    assert response.status_code == 302

    updated_user_post = UserPost.objects.get(pk=user_post.pk)
    assert updated_user_post.location == 'Test Location thoughtwin'
    assert updated_user_post.cap == 'Test Caption2'
    assert updated_user_post.desc == 'Test Description2'


# delete post
@pytest.mark.django_db
def test_delete_post(user,user_post):
    url = reverse('Post:delete_post',kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

# post detail
@pytest.mark.django_db
def test_post_detail(user,user_post):
    url = reverse('Post:post_detail',kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200