from django.urls import path
from .views import PostFilterView
app_name = 'filters'
urlpatterns = [
    path('posts/', PostFilterView.as_view(), name='filter_posts'),
]