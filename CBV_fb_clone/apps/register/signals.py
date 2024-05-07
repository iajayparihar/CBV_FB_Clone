from register.models import CustomUser
from django.dispatch import receiver 
from django.db.models.signals import post_save
import datetime
from django.contrib.auth.signals import user_logged_out,user_logged_in
from django.db.backends.signals import connection_created

@receiver(connection_created)
def connection_created_handler(sender, connection, **kwargs):
    current_time = datetime.datetime.now()
    with open("logdata.txt", 'a') as file:
        file.write(str(current_time) + '\t' + 'Database connection successfully.'+"\n")


@receiver(post_save, sender=CustomUser)
def UserPreSaveApi(sender, instance, created, **kwargs):
    current_time = datetime.datetime.now()
    if created:  # Only execute for newly created instances
        with open("logdata.txt", 'a') as file:
            file.write(str(current_time) + '\t' + instance.username + ' ' + 'User created successfully'+"\n")
    else:
        with open("logdata.txt", 'a') as file:
            file.write(str(current_time) + '\t' + instance.username + ' ' + 'Some changes in Database.'+"\n")

@receiver(user_logged_in)
def user_login(sender, request, **kwargs):
    current_time = datetime.datetime.now()
    with open("logdata.txt", 'a') as file:
        file.write(str(current_time) + '\t' + request.user.username + ' ' + 'User logout successfully.'+"\n")


@receiver(user_logged_out)
def user_logout(sender, request, **kwargs):
    current_time = datetime.datetime.now()
    with open("logdata.txt", 'a') as file:
        file.write(str(current_time) + '\t' + request.user.username + ' ' + 'User logout successfully.'+"\n")

