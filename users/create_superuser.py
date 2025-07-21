from django.contrib.auth import get_user_model

def create():
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            full_name='Admin User',
            phone_number='0000000000',
            country='N/A'
        )
        print("✔️ Superuser created.")
    else:
        print("ℹ️ Superuser already exists.")
