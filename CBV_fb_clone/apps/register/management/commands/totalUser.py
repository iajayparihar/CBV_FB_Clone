from django.core.management.base import BaseCommand
from register.models import CustomUser

class Command(BaseCommand):
    help = 'Displays stats related to CustomUser model'

    def handle(self, *args, **kwargs):
        total_users = CustomUser.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total Users: {total_users}'))
