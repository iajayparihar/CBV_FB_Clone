import pytest
from django.contrib.auth import get_user_model
from register.models import CustomUser

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
        'mobile': '1234567890',
        'DOB': '2000-01-01',
        'gender': 'Male'
    }

@pytest.fixture
def create_custom_user(user_data):
    return CustomUser.objects.create(**user_data)

@pytest.mark.django_db
def test_create_custom_user(create_custom_user, user_data):
    # Retrieve the created user from the database
    created_user = create_custom_user
    
    # Assert that the created user object is an instance of CustomUser
    assert isinstance(created_user, CustomUser)
    
    # Assert that the user's attributes match the provided values
    assert created_user.username == user_data['username']
    assert created_user.email == user_data['email']
    assert created_user.mobile == user_data['mobile']
    assert str(created_user.DOB) == user_data['DOB']
    assert created_user.gender == user_data['gender']
