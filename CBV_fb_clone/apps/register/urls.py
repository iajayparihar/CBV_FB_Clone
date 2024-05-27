from django.urls import path
from .views import *

app_name = "Register"
urlpatterns = [
    path('register/', register.as_view(), name='register'),
    path('profile/', profile.as_view(), name='profile'),
]
    # path('', user_login.as_view(), name='user_login'),

    # path('user_logout/', user_logout.as_view(), name='user_logout'),
