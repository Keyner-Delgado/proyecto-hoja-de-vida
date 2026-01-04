import os
from pathlib import Path
import dj_database_url

# 1. RUTAS BASE
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SEGURIDAD
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-tu-clave-aqui')

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
render_external_url = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_url:
    ALLOWED_HOSTS.append(render_external_url)

# 3. APLICACIONES INSTALADAS
INSTALLED_APPS = [
    'cloudinary_storage', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'cloudinary',
    'perfil',
]

# 4. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # DEBE estar justo debajo de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyectohojadevida.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'proyectohojadevida.wsgi.application'

# 5. BASE DE DATOS
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# 6. INTERNACIONALIZACIÓN
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# 7. ARCHIVOS ESTÁTICOS Y MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# --- CONFIGURACIÓN DE ALMACENAMIENTO (COMPATIBILIDAD CON CLOUDINARY Y WHITENOISE) ---
# Esta línea es necesaria para evitar el AttributeError que viste en Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Ajustes para diseño del Admin y seguridad en Render
WHITENOISE_USE_FINDERS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 8. CLOUDINARY
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'