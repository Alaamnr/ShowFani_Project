from django.urls import path
from .views import PostFilterView

urlpatterns = [
    path('posts/', PostFilterView.as_view(), name='filter_posts'),
]