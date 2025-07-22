# users/scripts/create_superuser.py (أو users/create_superuser.py إذا لم يتم نقله)

import os
import django
from django.contrib.auth import get_user_model
import sys 
import time 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showfani.settings')
django.setup()


print("Current Python paths (sys.path):")
for p in sys.path:
    print(f"  - {p}")
print("-" * 30)
print("Django settings module:", os.environ.get('DJANGO_SETTINGS_MODULE'))
print("-" * 30)

time.sleep(5) 
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