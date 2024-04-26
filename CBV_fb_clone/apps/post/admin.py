from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Like)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['user']
    
@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    '''Admin View for UserPost'''

    list_display = ('id','user')
    
@admin.register(UserComments)
class UserCommentsAdmin(admin.ModelAdmin):
    '''Admin View for UserComments'''

    list_display = ("id",'user','comment')
    