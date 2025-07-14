from django.shortcuts import render

from rest_framework import generics
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.permissions import AllowAny
from users.models import Artist, Investor

# Create your views here.
class PostFilterView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()

        art_section = self.request.query_params.get('art_section', None)
        user_type = self.request.query_params.get('user_type', None) 
        min_age = self.request.query_params.get('min_age', None)
        max_age = self.request.query_params.get('max_age', None)
        country = self.request.query_params.get('country', None)

        if art_section:
            queryset = queryset.filter(art_section=art_section.upper())

        if user_type:
            if user_type.lower() == 'artist':
                queryset = queryset.filter(owner__artist_profile__isnull=False)
            elif user_type.lower() == 'investor':
                queryset = queryset.filter(owner__investor_profile__isnull=False)

        if min_age:
            queryset = queryset.filter(owner__age__gte=min_age)
        if max_age:
            queryset = queryset.filter(owner__age__lte=max_age)

        if country:
            queryset = queryset.filter(owner__country__icontains=country)

        return queryset