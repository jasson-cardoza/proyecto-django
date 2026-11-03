"""Configuración de Django para ReciclaCerca."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Raíz del repositorio (la carpeta donde está manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Seguridad ---------------------------------------------------------------
# La clave secreta NO va en el código. Se lee de la variable de entorno
# DJANGO_SECRET_KEY (ver README.md > Variables de entorno). Para desarrollo
# local, si no existe, se usa una clave de prueba; en producción es obligatoria.

# SECURITY WARNING: don't run with debug turned on in production!
# Para apagarlo: DJANGO_DEBUG=False
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-clave-solo-para-desarrollo-local-no-usar-en-produccion'
    else:
        raise ImproperlyConfigured(
            'Falta la variable de entorno DJANGO_SECRET_KEY (obligatoria con DEBUG=False).'
        )

ALLOWED_HOSTS = []


# --- Aplicaciones ------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones del proyecto (responsabilidades en README.md > Estructura del proyecto)
    'inicio',     # Portada
    'usuarios',   # Cuentas, inicio de sesión, perfiles y direcciones
    'reciclaje',  # Materiales, puntos de reciclaje y registros de reciclaje
    'reportes',   # Reportes ciudadanos y su seguimiento
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# --- Plantillas --------------------------------------------------------------
# Las plantillas compartidas (base.html, includes/) están en templates/;
# las de cada app, en <app>/templates/<app>/.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# --- Base de datos (SQL Server Express) --------------------------------------
# El script database/ProyectoReciclaCerca.sql crea la base de datos.

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'ProyectoReciclaCerca',
        'HOST': 'localhost\\SQLEXPRESS',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'trusted_connection=yes;TrustServerCertificate=yes',
        },
    }
}


# --- Contraseñas -------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Sesión de usuario -------------------------------------------------------

LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'inicio:inicio'
LOGOUT_REDIRECT_URL = 'inicio:inicio'


# --- Idioma y hora -----------------------------------------------------------

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/El_Salvador'
USE_I18N = True
USE_TZ = True


# --- Archivos estáticos (CSS, JS, imágenes) ----------------------------------
# Nuestros archivos están en static/ (ej. static/css/estilos.css).

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# --- Correo ------------------------------------------------------------------
# En desarrollo los correos se imprimen en la consola.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
