
from django.urls import path
from .views import *
app_name = "Post"
urlpatterns = [
    path('post/', PostFormView.as_view(), name= 'post'),
    path('all_user_post/', all_user_post.as_view(), name= 'all_user_post'),
    path('view_post/', view_post.as_view(), name= 'view_post'),
    path('update_post/<int:pk>/', update_post.as_view(), name= 'update_post'),
    path('delete_post/<int:pk>/', delete_post.as_view(), name= 'delete_post'),
    path('post_detail/<int:pk>/', post_detail.as_view(), name= 'post_detail'),

    path('update_comment/', update_on_comment.as_view(), name='update_on_comment'),
    path('delete_comment/', delete_comment.as_view(), name='delete_comment'),
    
    path('post/comment/<int:pk>/', comment_on_post.as_view(), name='comment_on_post'),
    path('post/like/<int:pk>/', like.as_view() , name= 'like'),
]
