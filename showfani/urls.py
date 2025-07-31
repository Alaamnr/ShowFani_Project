from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [

    path('api/users/', include(('users.urls', 'users'), namespace='users')),
    path('api/posts/', include(('posts.urls', 'posts'), namespace='posts')),
    path('api/chat/', include(('chat.urls', 'chat'), namespace='chat')),
    path('api/filters/', include(('filters.urls', 'filters'), namespace='filters')),
    path('api/search/', include(('search.urls', 'search'), namespace='search')),
    path('api/app/', include(('app.urls', 'app'), namespace='app')),
    
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    

   # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 