from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserComments)
admin.site.register(Like)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['user']
    
admin.site.register(UserPost, UserPostAdmin)
    