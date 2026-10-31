
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j#@2-@#b@!_d-np^u(#0fgk7=skccf4dg@+*+2ly*3u)-&^i4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones del proyecto (responsabilidades en README.md > Estructura del proyecto)
    'inicio',     # Páginas públicas: portada e información general
    'usuarios',   # Cuentas, autenticación y perfiles
    'reciclaje',  # Dominio principal: materiales, puntos y registros de reciclaje
    'reportes',   # Estadísticas y reportes (solo lectura)
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

ROOT_URLCONF = 'Proyecto_ReciclaCerca.urls'

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

WSGI_APPLICATION = 'Proyecto_ReciclaCerca.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases


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

    #'segunda': {
     #   'ENGINE': 'mssql',
      #  'NAME': 'ProyectoReciclaCerca',
       # 'HOST': 'localhost\\SQLEXPRESS01',
        #'PORT': '',
        #'OPTIONS': {
         #   'python_driver': 'mssql_python',
          #  'extra_params': 'trusted_connection=yes;TrustServerCertificate=yes',
        #},
    #},
#}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'inicio:inicio'
LOGOUT_REDIRECT_URL = 'inicio:inicio'

import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']