# chat/admin.py
from django.contrib import admin
from .models import Chat, Message

# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):

    list_display = ('id', 'display_participants', 'created_at', 'updated_at')

    search_fields = ('participants__username',) 

 
    def display_participants(self, obj):
        return ", ".join([participant.username for participant in obj.participants.all()])
    display_participants.short_description = 'Participants' 

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('participants')
        return queryset

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'chat', 'sender', 'message_type', 'timestamp')
  
    search_fields = ('sender__username', 'text_content') 

    list_filter = ('message_type', 'timestamp', 'sender')
    
   
    fieldsets = (
        (None, {
            'fields': ('chat', 'sender', 'message_type',)
        }),
        ('Content', {
            'fields': ('text_content', 'file_attachment',)
        }),
        ('Timestamps', {
            'fields': ('timestamp',)
        }),
    )

    readonly_fields = ('timestamp',)