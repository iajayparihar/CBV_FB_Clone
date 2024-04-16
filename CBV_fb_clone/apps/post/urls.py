
from django.urls import path
from .views import *
app_name = "Post"
urlpatterns = [
    path('post/', PostFormView.as_view(), name= 'post'),
    path('dashboard/', dashboard.as_view(), name= 'dashboard'),
    path('all_user_post/', all_user_post.as_view(), name= 'all_user_post'),
    path('view_post/', view_post.as_view(), name= 'view_post'),
    path('update_post/<int:id>/', update_post.as_view(), name= 'update_post'),
    path('delete_post/<int:id>/', delete_post.as_view(), name= 'delete_post'),
    
    path('post_detail/<int:post_id>/', post_detail.as_view(), name= 'post_detail'),
    
    path('post/comment/<int:post_id>/', comment_on_post.as_view(), name='comment_on_post'),
    path('update_comment/', update_on_comment.as_view(), name='update_on_comment'),
    path('delete_comment/', delete_comment.as_view(), name='delete_comment'),
    
    path('post/like/<int:pk>/', like.as_view() , name= 'like'),
    path('post/unlike/<int:pk>/', unlike.as_view() , name= 'unlike'),
]
