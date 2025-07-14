from .models import Post
from django.contrib import admin

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
 
    list_display = ('owner_username', 'art_section', 'description_preview', 'views_count', 'created_at')
  
    search_fields = ('owner__username', 'owner__full_name', 'description')
  
    list_filter = ('art_section', 'created_at')
  
    ordering = ('-created_at',)
  
    raw_id_fields = ('owner',) 
 

    def owner_username(self, obj):
        return obj.owner.username
    owner_username.short_description = 'Owner Username'

    def description_preview(self, obj):
   
        return obj.description[:50] + '...' if obj.description and len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description Preview'