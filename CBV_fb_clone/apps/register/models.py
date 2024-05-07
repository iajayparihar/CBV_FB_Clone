from django.db import models
from django.contrib.auth.models import AbstractUser

gen = (("Female", 'Female'),
        ("Male", 'Male'),
        ('Trans','Trans'),
        ("Custom", 'Custom'),)

class CustomUser(AbstractUser):
    mobile = models.CharField( max_length=60)
    DOB = models.DateField(auto_now_add=False,blank=True,null=True)
    gender = models.CharField(max_length=60, choices=gen)
    
    def __str__(self):
        return self.username

from django.dispatch import receiver 
from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
import datetime
from django.contrib.auth.signals import user_logged_out

@receiver(post_save, sender=CustomUser)
def UserPreSaveApi(sender, instance, created, **kwargs):
    current_time = datetime.datetime.now()
    if created:  # Only execute for newly created instances
        with open("logdata.txt", 'a') as file:
            file.write(str(current_time) + '\t' + instance.username + ' ' + 'User created successfully'+"\n")
    else:
        with open("logdata.txt", 'a') as file:
            file.write(str(current_time) + '\t' + instance.username + ' ' + 'User successfully login.'+"\n")

@receiver(user_logged_out)
def user_logout(sender, request, **kwargs):
    current_time = datetime.datetime.now()
    with open("logdata.txt", 'a') as file:
        file.write(str(current_time) + '\t' + request.user.username + ' ' + 'User logout successfully.'+"\n")