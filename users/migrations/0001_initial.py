# Generated by Django 5.2.3 on 2025-06-19 12:54

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('country', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('ARTIST', 'Artist'), ('INVESTOR', 'Investor')], max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='artist_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('art_section', models.CharField(blank=True, choices=[('ACTING', 'Acting'), ('WRITING', 'Writing'), ('OTHER', 'Other')], max_length=50, null=True)),
                ('art_cv', models.FileField(blank=True, null=True, upload_to='artist_cvs/')),
                ('what_i_need', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='investor_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('support_type', models.CharField(choices=[('PAYMENT', 'Payment'), ('OTHER', 'Other')], max_length=50)),
                ('own_art_company', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_art_field', models.CharField(blank=True, max_length=255, null=True)),
                ('art_section', models.CharField(blank=True, choices=[('ACTING', 'Acting'), ('WRITING', 'Writing'), ('OTHER', 'Other')], max_length=50, null=True)),
                ('what_i_need', models.TextField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
