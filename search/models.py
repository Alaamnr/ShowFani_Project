   
from django.db import models
from users.models import CustomUser

class SearchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = 'Search Histories'
        indexes = [
            models.Index(fields=['user', 'searched_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} searched for '{self.query}' at {self.searched_at}"