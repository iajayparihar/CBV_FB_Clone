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

    