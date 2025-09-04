# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import datetime
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("ARTIST", "Artist"),
        ("INVESTOR", "Investor"),
    )
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    
    full_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=20, unique=True, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    age = models.PositiveIntegerField(blank=True, null=True) 
    profile_picture = CloudinaryField(resource_type='image', blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=False, null=False)


    REQUIRED_FIELDS = ['full_name', 'phone_number', 'country', 'date_of_birth', 'email']


    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = datetime.date.today()
            self.age = today.year - self.date_of_birth.year - \
                       ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Artist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='artist_profile')
    ART_SECTION_CHOICES = [
        ('ACTING', 'Acting'),
        ('WRITING', 'Writing'),
        ('SINGING', 'Singing'),
        ('DANCING', 'Dancing'),
        ('PAINTING', 'Painting'),
        ('SCULPTURE', 'Sculpture'),
        ('PHOTOGRAPHY', 'Photography'),
        ('MUSIC_COMPOSITION', 'Music Composition'),
        ('DIRECTING', 'Directing'),
        ('OTHER', 'Other'),
    ]
    art_section = models.CharField(max_length=50, choices=ART_SECTION_CHOICES, blank=True, null=True)
    artistic_bio = models.TextField(blank=True, null=True)
    artistic_achievements = models.TextField(blank=True, null=True)
  
    what_i_need = models.TextField(blank=True, null=True) 
 

    def __str__(self):
        return f"Artist: {self.user.full_name}"

class Investor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='investor_profile')
    SUPPORT_TYPE_CHOICES = [
        ('FINACIAL_SUPPORT', 'financial_support'),
        ('OTHER', 'Other'),
    ]
    ART_SECTION_CHOICES = [
        ('ACTING', 'Acting'),
        ('WRITING', 'Writing'),
        ('SINGING', 'Singing'),
        ('DANCING', 'Dancing'),
        ('PAINTING', 'Painting'),
        ('SCULPTURE', 'Sculpture'),
        ('PHOTOGRAPHY', 'Photography'),
        ('MUSIC_COMPOSITION', 'Music Composition'),
        ('DIRECTING', 'Directing'),
        ('OTHER', 'Other'),
    ]

    support_type = models.CharField(max_length=50, choices=SUPPORT_TYPE_CHOICES, blank=False, null=False)
    own_art_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_art_field = models.CharField(max_length=255, blank=True, null=True)
    art_section = models.CharField(max_length=50, choices=Artist.ART_SECTION_CHOICES, blank=True, null=True) 
    what_i_need = models.TextField(blank=True, null=True) 
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Investor: {self.user.full_name}"
    