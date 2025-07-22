from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count 
from django.utils import timezone 

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer , ChatCreateSerializer
from users.models import CustomUser


class ChatListCreateView(generics.ListCreateAPIView):

    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      
        return Chat.objects.filter(participants=self.request.user).prefetch_related('participants', 'messages').order_by('-updated_at')

   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatCreateSerializer
        return ChatSerializer 

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        other_user_id = serializer.validated_data.get('other_user_id')

        if str(other_user_id) == str(request.user.id):
            return Response({"detail": "لا يمكن إنشاء محادثة مع نفسك."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = CustomUser.objects.get(id=other_user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "المستخدم الآخر غير موجود."}, status=status.HTTP_404_NOT_FOUND)

    
        existing_chat = Chat.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).annotate(
            num_participants=Count('participants')
        ).filter(
            num_participants=2 
        ).first()

        if existing_chat:
          
            read_serializer = ChatSerializer(existing_chat, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        else:
         
            chat = Chat.objects.create()
            chat.participants.add(request.user, other_user)
   
            read_serializer = ChatSerializer(chat, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']

        try:
            chat = Chat.objects.get(id=chat_id)
      
            if self.request.user not in chat.participants.all():
                raise generics.PermissionDenied("أنت لست مشاركاً في هذه الدردشة.")
        except Chat.DoesNotExist:
            raise generics.NotFound("الدردشة غير موجودة.")


        return Message.objects.filter(chat_id=chat_id).order_by('timestamp')

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        try:
            chat = Chat.objects.get(id=chat_id)

            if self.request.user not in chat.participants.all():
                raise generics.PermissionDenied("أنت لست مشاركاً في هذه الدردشة.")
        except Chat.DoesNotExist:
            raise generics.NotFound("الدردشة غير موجودة.")

  
        serializer.save(sender=self.request.user, chat=chat)

        chat.updated_at = timezone.now()
        chat.save(update_fields=['updated_at'])
