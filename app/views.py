

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
import random 


class WelcomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Welcome to our App",
            "logo_url": "logo-url" 
        })

class HomePageView(generics.ListAPIView):

    serializer_class = PostSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
 
        queryset = Post.objects.all().order_by('?')[:20] 
        return queryset