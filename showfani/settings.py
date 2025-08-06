import dj_database_url
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent


#SECRET_KEY = 'django-insecure-^6#fzpjdmqwuzd)hb96k)iyy^a+vo91-o+p5-hl%km^@7d*v5u'


SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-^6#fzpjdmqwuzd)hb96k)iyy^a+vo91-o+p5-hl%km^@7d*v5u')

DEBUG = True

#DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'showfani-backend.onrender.com']

if not DEBUG:
 
    pass
#ALLOWED_HOSTS = []

"""ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

if not DEBUG:
    ALLOWED_HOSTS += [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
#............................"""
AUTH_USER_MODEL = 'users.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #my libraries
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt', 
    'rest_framework_simplejwt.token_blacklist',
    #'drf_spectacular',
    'cloudinary',
    'cloudinary_storage',
    
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'django_extensions',
  
    #my apps
    'users',
    'posts',
    'chat',
    'filters',
    'search',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',           
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'showfani.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'showfani.wsgi.application'
#ASGI_APPLICATION = 'showfani.asgi.application' 
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'), 
        conn_max_age=600,
        conn_health_checks=True,
    )

# showfani/settings.py

CORS_ALLOW_ALL_ORIGINS = True 


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6}, 
    },
 
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/' 


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


"""CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')      
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') """
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', 
}
"""

# CHANNEL_LAYERS

REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1') 

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "url": REDIS_URL, 
        },
    },
}
if os.environ.get('CREATE_SUPERUSER', 'False') == 'True':
    try:
        from users.create_superuser import create
        create()
    except Exception as e:
        print("Error creating superuser:", e)
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', # يمكن تغييرها لـ INFO في الإنتاج
            'class': 'logging.StreamHandler',
            'formatter': 'verbose', # استخدمي verbose هنا للحصول على تفاصيل أكثر
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG', # تأكدي أنها DEBUG أو INFO
            'propagate': False, # لا تدعها تنتشر للـ handlers الأخرى لتجنب التكرار
        },
        'django.request': { # لسجلات الطلبات والأخطاء
            'handlers': ['console'],
            'level': 'ERROR', # لضمان تسجيل أخطاء 500
            'propagate': False,
        },
        '': { # للـ root logger، يلتقط كل السجلات
            'handlers': ['console'],
            'level': 'INFO', # يمكن تغييرها لـ DEBUG للحصول على كل شيء
        },
    },
}
