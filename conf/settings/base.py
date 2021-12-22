"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import functools
from pathlib import Path
from apps.services.files.file import FileProcessingTool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
CONF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CONF_DIR)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
FILES_DIR = os.path.join(BASE_DIR, "files")
THEME_DIR = os.path.join(BASE_DIR, "themes")
ARCHIVE_DIR = os.path.join(FILES_DIR, "ARCHIVE")
NEWFILES_DIR = os.path.join(FILES_DIR, "NEW_FILES")
FileProcessingTool.check_and_create_dir(LOGS_DIR)
FileProcessingTool.check_and_create_dir(THEME_DIR)
FileProcessingTool.check_and_create_dir(ARCHIVE_DIR)
FileProcessingTool.check_and_create_dir(os.path.join(THEME_DIR, "static"))
# BASE_DIR = Path(__file__).resolve().parent.parent

# if not (os.path.exists(LOGS_DIR) and os.path.isdir(LOGS_DIR)):
#     os.makedirs(LOGS_DIR)


INTERNAL_IPS = ("127.0.0.1",)

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"

ANONYMOUS_URLS = [
    r"^admin/$",
    r"^admin/login/$",
    r"^media/",
    r"^static/",
]

# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "apps.repertoire",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

ALL_APPS_CONTAINER = {
    "DEFAULT_APPS": DEFAULT_APPS,
    "LOCAL_APPS": LOCAL_APPS,
    "THIRD_PARTY_APPS": THIRD_PARTY_APPS,
}

INSTALLED_APPS = functools.reduce(lambda x, y: x + y, ALL_APPS_CONTAINER.values())
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(THEME_DIR, "templates")],
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


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/var/www/media"

STATICFILES_DIRS = [
    os.path.join(THEME_DIR, "static"),
]

# AUTH_USER_MODEL = "user.UserProfile"

# FILEBROWSER
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [".pdf", ".doc", ".rtf", ".txt", ".xls", ".xlsx", ".csv", ".docx"],
    "Video": [".mov", ".mp4", ".m4v", ".webm", ".wmv", ".mpeg", ".mpg", ".avi", ".rm"],
    "Audio": [".mp3", ".wav", ".aiff", ".midi", ".m4p"],
    "Font": [".ttf"],
}

FILEBROWSER_DIRECTORY = ""
FILEBROWSER_OVERWRITE_EXISTING = False
FILEBROWSER_MAX_UPLOAD_SIZE = "104857600"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10MB

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s %(message)s - %(pathname)s#lines-%(lineno)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "default.log"),
            "formatter": "standard",
            "maxBytes": 104857600,
        },
        "handler_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "error.log"),
        },
        "daily_error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "daily_error.log"),
            "when": "midnight",
            "backupCount": 7,
            "formatter": "standard",
        },
        "handler_file_processor": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "file_processor.log"),
            "formatter": "standard",
            "maxBytes": 104857600,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["handler_error", "daily_error"],
            "level": "ERROR",
            "propagate": True,
        },
        "": {
            "handlers": ["default", "daily_error"],
            "level": "INFO",
            "propagate": True,
        },
        "file_processor": {
            "handlers": ["handler_file_processor", "daily_error"],
            "level": "INFO",
            "propagate": True,
        },
    },
}