from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ArtistRegisterView, InvestorRegisterView, CustomTokenObtainPairView,
    UserProfileView, PublicUserProfileView,ChangePasswordView,TestUploadView
)
app_name = 'users' 
urlpatterns = [
    path('register/artist/', ArtistRegisterView.as_view(), name='artist_register'),
    path('register/investor/', InvestorRegisterView.as_view(), name='investor_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<str:username>/', PublicUserProfileView.as_view(), name='public_user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('test-upload/', TestUploadView.as_view()),

]
    
