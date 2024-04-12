from django.db import models
from django.conf import settings

class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_post')
    location = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    cap = models.TextField(verbose_name='Caption', blank=True, null=True)
    desc = models.TextField(verbose_name='Description', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name}, {self.cap}"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_like')
    
    def __str__(self):
        return f"{self.user}, {self.post.user.username}"

class UserComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_comment')
    comment = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Logged in user: {self.user.first_name}, Comment:  {self.comment}"

