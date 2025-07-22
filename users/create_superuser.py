
# users/create_superuser.py

import os
import django 
from django.contrib.auth import get_user_model


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showfani.settings')
django.setup() 

def create():
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
        print(f"✔️ Superuser '{username}' created successfully.")
    else:
        print(f"ℹ️ Superuser '{username}' already exists.")

if __name__ == '__main__':

    create()