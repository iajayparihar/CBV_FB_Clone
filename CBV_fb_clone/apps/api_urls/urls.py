from django.urls import path,include
from api_views.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('',UserModelViewSet,basename='register')
    # path('register/', RegisterListCreateAPIView.as_view()),
    # path('register/<int:pk>/', RegisterRetrieveUpdateDestroyAPIView.as_view()),

urlpatterns = [
    path('register/',include(router.urls)),
    
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('profile/', ProfileApiView.as_view()),
    
    
    path('passChange/', PasswordChangeApiView.as_view()),
    path('post/', PostCreateAPIView.as_view(), name= 'post'),
    path('allpost/',AllPostAPIView.as_view()),
    path('postcrud/<int:pk>/',PostRetrieveUpdateDestroyAPIView.as_view()),
    
    path('like/<int:pk>/',LikeAPIView.as_view()),
    
    path('commets/<int:post_id>/',CommentsAPIView.as_view()),
    
]
