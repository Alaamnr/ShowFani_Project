from django.urls import path
from .views import WelcomeView, HomePageView
app_name = 'app' 
urlpatterns = [
    path('welcome/', WelcomeView.as_view(), name='welcome_page'),
    path('home/', HomePageView.as_view(), name='home_page_random_posts'),
]