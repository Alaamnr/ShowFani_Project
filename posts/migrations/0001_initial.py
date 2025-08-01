# Generated by Django 5.2.3 on 2025-06-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art_section', models.CharField(choices=[('ACTING', 'Acting'), ('WRITING', 'Writing'), ('OTHER', 'Other')], max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='post_pictures/')),
                ('video', models.FileField(blank=True, null=True, upload_to='post_videos/')),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
