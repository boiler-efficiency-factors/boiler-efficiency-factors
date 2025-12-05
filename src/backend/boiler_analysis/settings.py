from pathlib import Path
from datetime import timedelta
# ==============================================================================
# 0. 필수 설정 및 기본 경로 (BASICS)
# 1. 애플리케이션 정의 (APPLICATION DEFINITION)
# 2. 미들웨어 (MIDDLEWARE)
# 3. URL 및 템플릿 (URLS & TEMPLATES)
# 4. 국제화 (INTERNATIONALIZATION)
# 5. 보안 및 인증 (SECURITY & AUTHENTICATION)
# 6. 데이터베이스 (DATABASE)
# 7. 파일 관리 (FILES: Static, Media)
# 8. 서드파티 라이브러리 설정 (THIRD-PARTY SETTINGS: REST/CORS/JWT/Spectacular)
# 9. 로깅 (LOGGING)
# ==============================================================================


# ==============================================================================
# 0. 필수 설정 및 기본 경로 (BASICS)
# ==============================================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7$=ehtg7pqh4-+xpy)8qqh!qwghhwv*l99y1**rsh8fn*c6=&7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# 1. 애플리케이션 정의 (APPLICATION DEFINITION)
# ==============================================================================
INSTALLED_APPS = [
    # 1. Django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 2 서드파티 앱
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'drf_spectacular',

    # 3. 로컬 앱
    'boiler_analysis',
    'users'
]


# ==============================================================================
# 2. 미들웨어 (MIDDLEWARE)
# ==============================================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==============================================================================
# 3. URL 및 템플릿 (URLS & TEMPLATES)
# ==============================================================================
ROOT_URLCONF = 'boiler_analysis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'boiler_analysis.wsgi.application'


# ==============================================================================
# 4. 국제화 (INTERNATIONALIZATION)
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 5. 보안 및 인증 (SECURITY & AUTHENTICATION)
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# 6. 데이터베이스 (DATABASE)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# 7. 파일 관리 (FILES: Static, Media)
# ==============================================================================
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB


# ==============================================================================
# 8. 서드파티 라이브러리 설정 (THIRD-PARTY SETTINGS: REST/CORS/JWT/Spectacular)
# ==============================================================================
# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# JWT_AUTH settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False, # True 로 설정할 경우, TokenRefeshView 에 refresh token 을 보내면 새로운 access token 과 refresh token 이 반환
    'BLACKLIST_AFTER_ROTATION': True, # True시 기존에 있던 refresh token 은 blacklist 에 등록됨
    'TOKEN_USER_CLASS': 'instragram.User',
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # 생성된 토큰의 콘텐츠에 서명하는 데 사용되는 서명 키
    'AUTH_HEADER_TYPES': ('JWT',), # 인증에 사용할 인증 헤더 이름
}

# Spectacular settings (Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': '보일러 효율 분석 API',
    'DESCRIPTION': '보일러 효율 영향인자 분석을 위한 REST API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}


# ==============================================================================
# 9. 로깅 (LOGGING)
# ==============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'boiler_analysis': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}