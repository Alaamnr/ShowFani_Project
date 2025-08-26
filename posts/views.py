
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post
from .serializers import PostSerializer
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from cloudinary.uploader import upload

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views_count = F('views_count') + 1
        instance.save(update_fields=['views_count'])
        instance.refresh_from_db() 

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to edit this post."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        username = self.kwargs['username']
        return Post.objects.filter(owner__username=username)

class RandomPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny] 
    PAGE_SIZE = 10 

    def get_queryset(self):
        return Post.objects.order_by('?')[:self.PAGE_SIZE] 
    


class MediaUploadView(APIView):
  
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file was provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
   
            upload_result = upload(file_obj, resource_type='auto')
            
      
            if upload_result and 'secure_url' in upload_result:
                file_url = upload_result['secure_url']
                return Response({
                    "message": "File uploaded successfully.",
                    "file_url": file_url,
                    "public_id": upload_result['public_id']
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to upload file to Cloudinary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
