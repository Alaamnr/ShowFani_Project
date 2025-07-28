from django.urls import path
from .views import ChatListCreateView, MessageListCreateView
app_name = 'chat'
urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat_list_create'),
    path('<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message_list_create'),
]