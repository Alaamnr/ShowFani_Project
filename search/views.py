
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import SearchHistory
from posts.models import Post
from .serializers import SearchSerializer, SearchHistorySerializer
from users.models import CustomUser


from posts.serializers import PostSerializer
from users.serializers import UserSearchResultSerializer 

class SearchView(APIView):
  
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data['query']


        SearchHistory.objects.create(user=request.user, query=query)

        

        posts = Post.objects.filter(
            Q(description__icontains=query) |
            Q(owner__full_name__icontains=query)
        ).distinct().select_related('owner') 

        
        users = CustomUser.objects.filter(
            Q(full_name__icontains=query) |
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

        return Response({
            'posts': PostSerializer(posts, many=True).data,
            'users': UserSearchResultSerializer(users, many=True).data, 
            'search_query': query 
        }, status=status.HTTP_200_OK)


class SearchHistoryView(ListAPIView):
  
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
      
        return SearchHistory.objects.filter(user=self.request.user).order_by('-searched_at')

#زيادة حذف السجل 
class ClearSearchHistoryView(APIView):

    permission_classes = [IsAuthenticated] 
    def delete(self, request):
       
        deleted_count, _ = request.user.search_history.all().delete()
        return Response(
            {"detail": f"this contact is deleted{deleted_count}  from search history"},
            status=status.HTTP_204_NO_CONTENT #
        )