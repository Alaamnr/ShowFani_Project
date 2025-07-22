# users/management/commands/create_admin.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import sys 
import time 

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist using environment variables.'

    def handle(self, *args, **options):
        self.stdout.write("Running create_admin management command...")
        
      
        self.stdout.write("Current Python paths (sys.path):")
        for p in sys.path:
            self.stdout.write(f"  - {p}")
        self.stdout.write("-" * 30)
        self.stdout.write(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        self.stdout.write("-" * 30)

        time.sleep(5) 

        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        full_name = os.environ.get('DJANGO_SUPERUSER_FULLNAME', 'Admin User')
        phone_number = os.environ.get('DJANGO_SUPERUSER_PHONE_NUMBER', '0000000000')
        country = os.environ.get('DJANGO_SUPERUSER_COUNTRY', 'N/A')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number,
                country=country
            )
            self.stdout.write(self.style.SUCCESS(f"✔️ Superuser '{username}' created successfully."))
        else:
            self.stdout.write(self.style.NOTICE(f"ℹ️ Superuser '{username}' already exists."))