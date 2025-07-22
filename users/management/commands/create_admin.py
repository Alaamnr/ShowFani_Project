
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import sys
import time
from datetime import date 

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist using environment variables.'

    def handle(self, *args, **options):
        self.stdout.write("Running create_admin management command...")

   

        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        full_name = os.environ.get('DJANGO_SUPERUSER_FULLNAME', 'Admin User')
        phone_number = os.environ.get('DJANGO_SUPERUSER_PHONE_NUMBER', '0000000000')
        country = os.environ.get('DJANGO_SUPERUSER_COUNTRY', 'N/A')

        date_of_birth = os.environ.get('DJANGO_SUPERUSER_DOB', '2000-01-01')

        try:
            year, month, day = map(int, date_of_birth.split('-'))
            date_of_birth_obj = date(year, month, day)
        except ValueError:
            self.stderr.write(self.style.ERROR(f"Error parsing date of birth: {date_of_birth}. Using default 2000-01-01."))
            date_of_birth_obj = date(2000, 1, 1)

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number,
                country=country,
                date_of_birth=date_of_birth_obj, 
            )
            self.stdout.write(self.style.SUCCESS(f"✔️ Superuser '{username}' created successfully."))
        else:
            self.stdout.write(self.style.NOTICE(f"ℹ️ Superuser '{username}' already exists."))