
from django.contrib import admin
from .models import SearchHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    
    list_display = ('user_username', 'query', 'searched_at')

    search_fields = ('query', 'user__username', 'user__full_name')
 
    list_filter = ('searched_at',)
 
    ordering = ('-searched_at',)
  
    readonly_fields = ('user', 'query', 'searched_at') 

 
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User' 