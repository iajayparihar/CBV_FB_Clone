from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()
class Command(BaseCommand):
    help = 'Creates a staff user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the new staff user')
        parser.add_argument('--email', type=str, help='Email for the new staff user')
        parser.add_argument('--password', type=str, help='Password for the new staff user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
    
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('User already exists.'))
            return
        
        staff_user = User.objects.create_user(username=username, email=email, password=password)
        staff_user.is_staff = True
        staff_user.save()
        
        self.stdout.write(self.style.SUCCESS('Staff user created successfully.'))
