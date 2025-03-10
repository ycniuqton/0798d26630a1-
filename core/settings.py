"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os, random, string, inspect
from pathlib import Path
from dotenv import load_dotenv
from str2bool import str2bool
from django.utils.translation import gettext_lazy as _

import config
from config import *
import dj_database_url

import django_dyn_dt

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

# Enable/Disable DEBUG Mode
DEBUG = str2bool(os.environ.get('DEBUG'))
# print(' DEBUG -> ' + str(DEBUG) )

ALLOWED_HOSTS = ['*']

# Add here your deployment HOSTS
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:5085', 'http://127.0.0.1:8000',
                        'http://127.0.0.1:5085', 'https://worldsever.com']

X_FRAME_OPTIONS = "SAMEORIGIN"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# multiple language
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('vi', _('Vietnamese')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Application definition

INSTALLED_APPS = [
    'admin_datta.apps.AdminDattaConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_spectacular",
    "home",
    "api",

    # Tooling Dynamic_DT
    'django_dyn_dt',  # <-- NEW: Dynamic_DT
    'rest_framework_simplejwt.token_blacklist',

    # Tooling API-GEN
    'django_api_gen',  # Django API GENERATOR  # <-- NEW
    'rest_framework',  # Include DRF           # <-- NEW
    'rest_framework.authtoken',  # Include DRF Auth      # <-- NEW     
]

MIDDLEWARE = [
    'core.middleware.CustomAuthMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'core.middleware.ContextIDMiddleware',

]

ROOT_URLCONF = "core.urls"

HOME_TEMPLATES = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIR_DATATB = os.path.join(BASE_DIR, "django_dyn_dt/templates")  # <-- NEW: Dynamic_DT

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [HOME_TEMPLATES, TEMPLATE_DIR_DATATB],  # <-- UPD: Dynamic_DT
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.my_constants",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_ENGINE = os.getenv('DB_ENGINE', None)
DB_USERNAME = os.getenv('DB_USERNAME', None)
DB_PASS = os.getenv('DB_PASS', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)

DATABASES = {'default': dj_database_url.config(default=PGDBConfig.DB_URI)}

# if DB_ENGINE and DB_NAME and DB_USERNAME:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.' + DB_ENGINE,
#             'NAME': DB_NAME,
#             'USER': DB_USERNAME,
#             'PASSWORD': DB_PASS,
#             'HOST': DB_HOST,
#             'PORT': DB_PORT,
#         },
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'db.sqlite3',
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

handler404 = 'home.views.common.404.custom_404'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DYN_DB_PKG_ROOT = os.path.dirname(inspect.getfile(django_dyn_dt))  # <-- NEW: Dynamic_DT

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(DYN_DB_PKG_ROOT, "templates/static"),  # <-- NEW: Dynamic_DT
)

# if not DEBUG:
#    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ### DYNAMIC_DATATB Settings ###
DYNAMIC_DATATB = {
    # SLUG -> Import_PATH 
    'product': "home.models.Product",
}
########################################

# ### API-GENERATOR Settings ###
API_GENERATOR = {
    # SLUG -> Import_PATH 
    'product': "home.models.Product",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'core.authentication.APIKeyAuthentication',
        'core.authentication.CookieBasicAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated'

    ),
    'EXCEPTION_HANDLER': 'core.exception_handlers.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTHENTICATION_BACKENDS = [
    'core.authentication_backends.EmailOrUsernameModelBackend',  # Add the path to your custom backend
    'django.contrib.auth.backends.ModelBackend',  # Django's default authentication backend
]

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

AUTH_USER_MODEL = 'home.User'

USE_TZ = True  # This ensures that Django stores datetimes in UTC
TIME_ZONE = 'UTC'  # Or any other timezone you are working with

SPECTACULAR_SETTINGS = {
    'TITLE': f'{APPConfig.APP_NAME} API Documentation',
    'DESCRIPTION': '''<div style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2 style="color: #2b7de9;">Detailed API Documentation</h2>
    <p>
        Welcome to the API documentation. This API offers comprehensive access to manage VPS instances, 
        with customizable options and filterable endpoints for efficient data retrieval.
    </p>
    <h3 style="color: #333; margin-top: 20px;">Authentication Methods</h3>
    <p>
        <strong>APIKeyAuth</strong> - This API requires an API key for authorization.
        <br>
        <em style="color: #888;">To use the API, add the API key as a header in each request:</em><br>
        <code style="background: #f4f4f4; padding: 4px 8px; border-radius: 4px;">
            x-api-key: YOUR_API_KEY
        </code>
    </p>
    <h3 style="color: #333; margin-top: 20px;">Getting Your API Key</h3>
    <p>
        To obtain an API key, go to <strong>Dashboard &gt; Account &gt; Authentication</strong>. Here, you can:
    </p>
    <ul>
        <li>Create a new API key by clicking <strong>"Generate New Key"</strong>.</li>
        <li>Use your default API key if one is already provided.</li>
    </ul>
    <p style="color: #888;">Keep your API key secure and avoid sharing it publicly.</p>
</div>
''',
    'VERSION': '1.0.0',
    'DEFAULT_AUTO_SCHEMA_CLASS': None,
    'PREPROCESSING_HOOKS': ['core.drf.preprocess_exclude_paths'],
}

from core.drf.extentions import APIKeyAuthenticationExtension
