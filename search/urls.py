from django.urls import path
from .views import SearchView, SearchHistoryView, ClearSearchHistoryView
app_name = 'search'
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('search/history/', SearchHistoryView.as_view(), name='search_history'),
    path('search/history/clear/', ClearSearchHistoryView.as_view(), name='clear_search_history'),
]