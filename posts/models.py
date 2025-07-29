from django.db import models
from users.models import CustomUser
from cloudinary.models import CloudinaryField

class Post(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    ART_SECTION_CHOICES = [
        ('ACTING', 'Acting'),
        ('WRITING', 'Writing'),
        ('OTHER', 'Other'),
    ]
    art_section = models.CharField(max_length=50, choices=ART_SECTION_CHOICES, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    picture = CloudinaryField(resource_type='image', blank=True, null=True)
    video = CloudinaryField(resource_type='video', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
    
        if not (self.description or self.picture or self.video):
            from django.core.exceptions import ValidationError
            raise ValidationError("A post must have at least one of: description, picture, or video.")

    def __str__(self):
        return f"Post by {self.owner.username} - {self.art_section}"