"""
Django settings for onpremise_service project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from identity.django import Auth
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


client_id = os.getenv("APP_ID")
client_secret = os.getenv("SECRET_ENTRA")
authority = "https://login.microsoftonline.com/alephsub0.org"
redirect_uri = "https://servicios-onpremise.alephsub0.org/authentraredirect"


AUTH = Auth(
    client_id,
    client_credential=client_secret,
    authority=authority,
    redirect_uri=redirect_uri,
)


MAC_ADDRESS_SFS = os.getenv("MAC_ADDRESS_SFS")
IP_SFS = os.getenv("IP_SFS")
USER_SFS = os.getenv("USER_SFS")
TIPO_SFS = os.getenv("TIPO_SFS")
MAC_ADDRESS_PDW = os.getenv("MAC_ADDRESS_PDW")
IP_PDW = os.getenv("IP_PDW")
USER_PDW = os.getenv("USER_PDW")
TIPO_PDW = os.getenv("TIPO_PDW")
SSH_KEY_NAME = os.getenv("SSH_KEY_NAME")
GRUPO_RECURSOS_DESARROLLO = os.getenv("GRUPO_RECURSOS_DESARROLLO")
GRUPO_RECURSOS_PRODUCCION = os.getenv("GRUPO_RECURSOS_PRODUCCION")

CLAVE_API_AZURE = os.getenv("CLAVE_API_AZURE")
RUTA_API_CLOUD_VM = "https://api-prd.alephsub0.org/api/v1/cloud/az/vm/"

dict_servidores = {
    "servidor_sfsdfs": {
        "servidor": MAC_ADDRESS_SFS,
        "ip": IP_SFS,
        "usuario": USER_SFS,
        "tipo": TIPO_SFS,
    },
    "servidor_pdweaf": {
        "servidor": MAC_ADDRESS_PDW,
        "ip": IP_PDW,
        "usuario": USER_PDW,
        "tipo": TIPO_PDW,
    },
    "servidor_qfgql": {
        "nombre_vm": "srv-dev-worker-1",
        "grupo_recursos": GRUPO_RECURSOS_PRODUCCION
    },
    "servidor_ndlql": {
        "nombre_vm": "srv-dev-worker-2",
        "grupo_recursos": GRUPO_RECURSOS_DESARROLLO
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "identity",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "onpremise_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "onpremise_service.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SECURE_CROSS_ORIGIN_OPENER_POLICY = None


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "/"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = "/srv/www/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

CRISPY_TEMPLATE_PACK = "bootstrap4"
