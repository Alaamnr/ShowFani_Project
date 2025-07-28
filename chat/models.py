from django.db import models
from users.models import CustomUser
from cloudinary.models import CloudinaryField
class Chat(models.Model):
  
    participants = models.ManyToManyField(
        CustomUser,
        related_name='chats',
        limit_choices_to={'is_active': True} 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      
        return f"Chat ID: {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')

    MESSAGE_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('AUDIO', 'Audio'),
        ('FILE', 'File'),
    ]
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='TEXT'
    )
    
 
    text_content = models.TextField(blank=True, null=True) 
    
    file_attachment = models.FileField(
        upload_to='chat_attachments/', 
        blank=True,
        null=True,
        max_length=255 
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] 

    def clean(self):
        from django.core.exceptions import ValidationError
        
        content_fields_filled = []
        if self.text_content:
            content_fields_filled.append('text_content')
        if self.file_attachment:
            content_fields_filled.append('file_attachment')

        if len(content_fields_filled) != 1:
            raise ValidationError("A message must have exactly one type of content: either text, or a file attachment (audio/file).")
        
     
        if self.text_content and self.message_type != 'TEXT':
            raise ValidationError("If text content is present, message_type must be 'TEXT'.")
        
        if self.file_attachment and self.message_type == 'TEXT':
            raise ValidationError("If a file attachment is present, message_type cannot be 'TEXT'. It must be 'AUDIO' or 'FILE'.")

        if self.file_attachment and self.message_type not in ['AUDIO', 'FILE']:
            raise ValidationError("If a file attachment is present, message_type must be 'AUDIO' or 'FILE'.")

    def __str__(self):
        return f"Message from {self.sender.username} in Chat {self.chat.id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"