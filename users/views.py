# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    ArtistRegistrationSerializer, InvestorRegistrationSerializer,
    UserProfileDetailSerializer, CustomUserSerializer,
    ArtistProfileSerializer, InvestorProfileSerializer ,CustomTokenObtainPairSerializer,ChangePasswordSerializer 
)
from .models import CustomUser, Artist, Investor
import cloudinary.uploader
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser
class ArtistRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ArtistRegistrationSerializer

class InvestorRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = InvestorRegistrationSerializer


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,) 
    model = CustomUser
    #permission_classes = (AllowAny,)

    
   # def get_object(self, queryset=None):
   #     return None
    def get_object(self):
    
        return self.request.user

    def update(self, request, *args, **kwargs):
       # serializer = self.get_serializer(data=request.data)
        serializer = self.get_serializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
   
        serializer.save() 
        return Response({"detail": "تم تغيير كلمة السر بنجاح."}, status=status.HTTP_200_OK)



class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
   
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #user_serializer = CustomUserSerializer(instance, data=request.data, partial=partial)
        user_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        user_serializer.is_valid(raise_exception=True)
      
        if 'user_type' in user_serializer.validated_data:
            user_serializer.validated_data.pop('user_type') 
        user_serializer.save()

        if hasattr(instance, 'artist_profile'):
            artist_data = request.data.get('artist_profile')
            if artist_data:
                artist_serializer = ArtistProfileSerializer(instance.artist_profile, data=artist_data, partial=partial)
                artist_serializer.is_valid(raise_exception=True)
                artist_serializer.save()
        elif hasattr(instance, 'investor_profile'):
            investor_data = request.data.get('investor_profile')
            if investor_data:
                investor_serializer = InvestorProfileSerializer(instance.investor_profile, data=investor_data, partial=partial)
                investor_serializer.is_valid(raise_exception=True)
                investor_serializer.save()


        full_serializer = self.get_serializer(instance)
        return Response(full_serializer.data)

class PublicUserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [AllowAny] 
    lookup_field = 'username'



class TestUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        result = cloudinary.uploader.upload(file)
        return Response({'url': result['secure_url']})
