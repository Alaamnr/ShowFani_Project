from django.urls import path
from .views import SearchView, SearchHistoryView, ClearSearchHistoryView
app_name = 'search'
urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('history/', SearchHistoryView.as_view(), name='search_history'),
    path('history/clear/', ClearSearchHistoryView.as_view(), name='clear_search_history'),
]