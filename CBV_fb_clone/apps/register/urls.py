from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='user_login'),
    path('user_logout', user_logout, name='user_logout'),
]