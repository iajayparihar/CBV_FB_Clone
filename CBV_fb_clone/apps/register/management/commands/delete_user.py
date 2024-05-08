from django.core.management.base import BaseCommand
from register.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import Http404
class Command(BaseCommand):
    help = 'Displays stats related to CustomUser model'
    
    def add_arguments(self, parser):
        parser.add_argument('--delete', type=str, help='delete a user from this cmd')

    def handle(self, *args, **kwargs):      
        try:
            user = get_object_or_404(CustomUser, username=kwargs['delete'])
            user.delete()
            self.stdout.write(self.style.SUCCESS('User Deleted successfully'))
        except Http404:
            self.stdout.write(self.style.ERROR('User not found.'))
