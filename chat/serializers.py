from rest_framework import serializers
from .models import Chat, Message

from users.serializers import UserProfileDetailSerializer 
from users.models import CustomUser

class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'profile_picture', 'user_type']
        read_only_fields = fields 

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_profile_picture = serializers.ImageField(source='sender.profile_picture', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'sender_username', 'sender_profile_picture',
            'message_type', 'text_content', 'file_attachment', 'timestamp'
        ]
        read_only_fields = ['id', 'chat', 'sender', 'sender_username', 'sender_profile_picture', 'timestamp']

    def validate(self, data):

        text_content_provided = bool(data.get('text_content'))
        file_attachment_provided = bool(data.get('file_attachment'))

    
        if not (text_content_provided ^ file_attachment_provided): 
            raise serializers.ValidationError("A message must have exactly one type of content: either 'text_content' or 'file_attachment'.")
        
        message_type = data.get('message_type', 'TEXT')

      
        if text_content_provided:
            if message_type != 'TEXT':
                raise serializers.ValidationError("If 'text_content' is provided, 'message_type' must be 'TEXT'.")
        elif file_attachment_provided:
            if message_type not in ['AUDIO', 'FILE']:
                raise serializers.ValidationError("If 'file_attachment' is provided, 'message_type' must be 'AUDIO' or 'FILE'.")
        
        return data

class ChatSerializer(serializers.ModelSerializer):

    other_participant = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField() 

    class Meta:
        model = Chat
        fields = ['id', 'other_participant', 'created_at', 'updated_at', 'last_message']
        read_only_fields = ['id', 'created_at', 'updated_at', 'other_participant', 'last_message']

    def get_other_participant(self, obj):
   
        request = self.context.get('request')
        current_user = request.user if request else None

        other_participants = [p for p in obj.participants.all() if p != current_user]
        
        if other_participants:
       
            return ChatParticipantSerializer(other_participants[0], context={'request': request}).data
        return None 

    def get_last_message(self, obj):
     
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

   