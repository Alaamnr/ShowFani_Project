from django.urls import path
from .views import PostListCreateView, PostDetailView, UserPostsView, RandomPostsView,MediaUploadView
app_name = 'posts'
urlpatterns = [
    path('create/', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('user/<str:username>/', UserPostsView.as_view(), name='user_posts'),
    path('random/', RandomPostsView.as_view(), name='random_posts'),
    path('upload/', MediaUploadView.as_view(), name='media_upload'),
]