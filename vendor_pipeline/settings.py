import os
from pathlib import Path
import environ
from dotenv import load_dotenv

# ============================================================================
# LOAD ENVIRONMENT VARIABLES FROM .env
# ============================================================================

load_dotenv()
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(str, 'localhost'),
)
environ.Env.read_env()

# ============================================================================
# BASE CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env('DEBUG', default=True)
SECRET_KEY = env('SECRET_KEY', default='dev-secret-key-change-in-production-12345678')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    
    # Local
    'pipeline',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vendor_pipeline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'vendor_pipeline.wsgi.application'

# ============================================================================
# DATABASE CONFIGURATION - POSTGRESQL VIA DATABASE_URL
# ============================================================================

# Read DATABASE_URL from .env file
# Format: postgresql://vendor_user:your_strong_password_here@localhost:5432/vendor_pipeline
# Set USE_SQLITE=true in .env to use SQLite instead

USE_SQLITE = os.getenv('USE_SQLITE', 'false').lower() == 'true'

if USE_SQLITE:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://vendor_user:password@localhost:5432/vendor_pipeline')

    from urllib.parse import urlparse, unquote

    parsed = urlparse(DATABASE_URL)
    if parsed.scheme and parsed.scheme.startswith('postgres'):
        username = unquote(parsed.username) if parsed.username else os.getenv('DATABASE_USER', 'vendor_user')
        password = unquote(parsed.password) if parsed.password else os.getenv('DATABASE_PASSWORD', 'password')
        host = parsed.hostname or os.getenv('DATABASE_HOST', 'localhost')
        port = str(parsed.port) if parsed.port else os.getenv('DATABASE_PORT', '5432')
        database = parsed.path.lstrip('/') or os.getenv('DATABASE_NAME', 'vendor_pipeline')

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': database,
                'USER': username,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,

                # Performance & Reliability Settings
                'ATOMIC_REQUESTS': True,        # Each request is a transaction
                'CONN_MAX_AGE': 600,            # Connection pooling (10 minutes)

                # SSL Configuration & timeouts
                'OPTIONS': {
                    'sslmode': 'prefer',        # Use SSL if available
                    'connect_timeout': 10,      # Connection timeout in seconds
                    'options': f"-c statement_timeout=30000",  # 30s statement timeout
                }
            }
        }
    else:
        # Fallback to default PostgreSQL connection
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DATABASE_NAME', 'vendor_pipeline'),
                'USER': os.getenv('DATABASE_USER', 'vendor_user'),
                'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
                'HOST': os.getenv('DATABASE_HOST', 'localhost'),
                'PORT': os.getenv('DATABASE_PORT', '5432'),
                
                'ATOMIC_REQUESTS': True,
                'CONN_MAX_AGE': 600,
                'AUTOCOMMIT': False,
                
                'OPTIONS': {
                    'sslmode': 'prefer',
                    'connect_timeout': 10,
                }
            }
        }

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/hour',
        'user': '10000/hour'
    },
    
    # Custom exception handler for consistent error responses
    'EXCEPTION_HANDLER': 'vendor_pipeline.exception_handler.custom_exception_handler',
    
    # Default renderer for JSON responses
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
    # Datetime format for consistent serialization
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
}

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8501",
    "http://frontend:8501",
    "http://frontend:8501",
    "http://backend:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Create logs directory if it doesn't exist
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'pipeline.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'django.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'db_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'database.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    
    'loggers': {
        'pipeline': {
            'handlers': ['console', 'file'],
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================================
# AZURE OPENAI CONFIGURATION
# ============================================================================

AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
AZURE_API_VERSION = os.getenv('AZURE_API_VERSION', '2025-01-01-preview')

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
# ============================================================================
# DJANGO REST FRAMEWORK
# ============================================================================
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer',
#     ),
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
#     'EXCEPTION_HANDLER': 'vendor_pipeline.exception_handler.custom_exception_handler',
# }
# ============================================================================
# SIMPLE JWT
# ============================================================================