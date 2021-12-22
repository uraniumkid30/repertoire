from .base import *
import environ
from decouple import config


ROOT_DIR = environ.Path(__file__) - 2
env_file = ROOT_DIR(".env")
env = environ.Env()
env.read_env(env_file)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="*")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="")
DJANGO_ENV = env.str("DJANGO_ENV", default="development")


if DJANGO_ENV == "development":
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

if DJANGO_ENV == "development":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "testDB.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT", cast=int),
        }
    }
