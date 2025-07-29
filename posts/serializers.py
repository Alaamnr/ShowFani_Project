from rest_framework import serializers
from .models import Post
from users.models import Artist, Investor 
from cloudinary.models import CloudinaryField

class PostSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_full_name = serializers.CharField(source='owner.full_name', read_only=True)
    owner_type = serializers.SerializerMethodField()
    
    owner_profile_picture = serializers.SerializerMethodField()
    content_types = serializers.SerializerMethodField()

    picture = serializers.FileField(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    

  
    owner_id_type = serializers.SerializerMethodField()
    def get_owner_profile_picture(self, obj):
      pic = getattr(obj.owner, 'profile_picture', None)
      return pic.url if pic else None
    

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'owner_username', 'owner_full_name', 'owner_type',
            'art_section',  'owner_id_type', 'owner_profile_picture', 'content_types','description', 'picture', 'video', 'views_count', 'created_at'
        ]
        read_only_fields = ['owner', 'views_count', 'created_at', 'updated_at','id']

    def get_owner_type(self, obj):
        if hasattr(obj.owner, 'artist_profile'):
            return 'artist'
        elif hasattr(obj.owner, 'investor_profile'):
            return 'investor'
        return 'unknown'
    def get_content_types(self, obj):
    
        types = []
        if obj.description:
            types.append('text')
        if obj.picture:
            types.append('image')
        if obj.video:
            types.append('video')
        return types


    def get_owner_id_type(self, obj):
        try:
            if hasattr(obj.owner, 'artist_profile') and obj.owner.artist_profile is not None:
              
                return obj.owner.artist_profile.pk
            elif hasattr(obj.owner, 'investor_profile') and obj.owner.investor_profile is not None:
        
                return obj.owner.investor_profile.pk
        except (Artist.DoesNotExist, Investor.DoesNotExist):
      
         
            pass
        return None


    def validate(self, data):
     
        if not (data.get('description') or data.get('picture') or data.get('video')):
            raise serializers.ValidationError("A post must have at least one of: description, picture, or video.")
        return data
    
