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
