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


@pytest.fixture
def user_comment(user, user_post):
    return UserComments.objects.create(user=user, post=user_post, comment="first comment")


@pytest.mark.django_db
def test_post_form_view(user):
    url = reverse('Post:post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_form_submission(user):
    client.force_login(user)
    url = reverse('Post:post')
    data = {'image': 'test_image.jpg', 'location': 'Test Location', 'cap': 'Test Caption', 'desc': 'Test Description'}
    response = client.post(url, data, format='multipart')
    assert response.status_code == 200


@pytest.mark.django_db
def test_like(user, user_post):
    client.force_login(user)
    url = reverse('Post:like', kwargs={'pk': user_post.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_on_post_view(user, user_post):
    url = reverse('Post:comment_on_post', kwargs={'pk': user_post.pk})
    client.force_login(user)
    data = {'comment': 'Test comment'}
    response = client.post(url, data)
    assert response.status_code == 200
    cmt = UserComments.objects.get(user=user, post=user_post)
    assert cmt.comment == 'Test comment'


@pytest.mark.django_db
def test_view_post(user):
    url = reverse('Post:view_post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_user_post_show(user):
    url = reverse('Post:all_user_post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_post_get(user, user_post):
    url = reverse('Post:update_post', kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_post_POST(user, user_post):
    url = reverse('Post:update_post', kwargs={'pk': user_post.pk})
    client.force_login(user)
    data = {'image': 'test_image2.jpg', 'location': 'Test Location thoughtwin', 'cap': 'Test Caption2', 'desc': 'Test Description2'}
    response = client.post(url, data=data, format='multipart')
    assert response.status_code == 302
    updated_user_post = UserPost.objects.get(pk=user_post.pk)
    assert updated_user_post.location == 'Test Location thoughtwin'
    assert updated_user_post.cap == 'Test Caption2'
    assert updated_user_post.desc == 'Test Description2'


@pytest.mark.django_db
def test_delete_post(user, user_post):
    url = reverse('Post:delete_post', kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail(user, user_post):
    url = reverse('Post:post_detail', kwargs={'pk': user_post.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_comment_post(user, user_comment, user_post):
    url = reverse('Post:update_on_comment')
    client.force_login(user)
    cmt_pk = user_comment.pk
    data = {'comment': 'Test comment new !!', "cmt_id": cmt_pk}
    response = client.post(url, data)
    assert response.status_code == 200
    cmt = UserComments.objects.get(user=user, post=user_post)
    assert cmt.comment == 'Test comment new !!'


@pytest.mark.django_db
def test_delete_comment(user, user_comment):
    url = reverse('Post:delete_comment')
    client.force_login(user)
    cmt_pk = user_comment.pk
    data = {"cmt_id": cmt_pk}
    response = client.get(url, data)
    assert response.status_code == 200
    with pytest.raises(UserComments.DoesNotExist):
        UserComments.objects.get(pk=cmt_pk)


@pytest.mark.django_db
def test_delete_non_existing_post(user):
    url = reverse('Post:delete_post', kwargs={'pk': 123})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_non_existing_comment_post(user):
    url = reverse('Post:update_on_comment')
    client.force_login(user)
    data = {'comment': 'Test comment new !!', "cmt_id": 456}
    response = client.post(url, data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_post_detail_non_existing_post(user):
    url = reverse('Post:post_detail', kwargs={'pk': 123})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 404




@pytest.mark.django_db
def test_all_user_post_view(user):
    # Create some sample user posts
    user_post1 = UserPost.objects.create(user=user, image='test_image1.jpg', location='Test Location1', cap='Test Caption1', desc='Test Description1')
    user_post2 = UserPost.objects.create(user=user, image='test_image2.jpg', location='Test Location2', cap='Test Caption2', desc='Test Description2')
    
    user_comment1 = UserComments.objects.create(user=user, post=user_post1, comment="first comment1")
    user_comment2 = UserComments.objects.create(user=user, post=user_post2, comment="first comment2")

    Like.objects.create(user=user, post=user_post1)
    
    client = Client()
    client.force_login(user)
    response = client.get(reverse('Post:all_user_post'))
    
    assert response.status_code == 200
    assert user_post1 in response.context_data['all_user_post']  
    assert user_post2 in response.context_data['all_user_post']  
    assert len(response.context_data['comment']) == 2
    assert response.context_data['userpost_list'][0].like== 0   