
from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
#from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Showfani Project API", 
      default_version='v1',
      description="توثيق شامل لواجهة برمجة التطبيقات (API) لتطبيق Showfani.",
      terms_of_service="https://www.google.com/policies/terms/", # اختياري: رابط شروط الخدمة الخاص بك
      contact=openapi.Contact(email="your_email@example.com"), # اختياري: بريدك الإلكتروني للتواصل
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/filters/', include('filters.urls')), 
    path('api/search/', include('search.urls')),  
    path('api/app/', include('app.urls')),
    path('admin/', admin.site.urls),

    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)