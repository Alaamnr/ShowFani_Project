# Generated by Django 5.2.3 on 2025-07-13 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_artist_art_cv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='art_cv',
            new_name='artistic_achievements',
        ),
        migrations.AddField(
            model_name='artist',
            name='artistic_bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
