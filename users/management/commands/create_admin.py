import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin user from environment variables'

    def handle(self, *args, **options):
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        if not admin_password:
            self.stdout.write(
                self.style.ERROR('ADMIN_PASSWORD environment variable is required')
            )
            return
        
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{admin_username}" already exists')
            )
            return
        
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Admin user "{admin_username}" created successfully')
        )
