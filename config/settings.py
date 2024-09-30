from pathlib import Path
import os

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для проекта Django. 
# В продакшене его следует хранить в защищённом месте.
SECRET_KEY = 'django-insecure-=d%6up6murt+28z1)=_cjwe=g6))iysv&g6u$dhx8l$@-^obqs'

# Включение отладки. В продакшене DEBUG должен быть False.
DEBUG = True

# Список разрешённых хостов для вашего проекта.
ALLOWED_HOSTS = []

# Определение установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'catalog',
    'django_apscheduler',
    'mail.apps.MailConfig',  # Измените на конфигурацию приложения
]

# Определение промежуточного ПО
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

# Конфигурация шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users', 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Конфигурация базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'screencast',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Валидация паролей
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

# Настройки интернационализации
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Медиафайлы (пользовательский контент)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'users.CustomUser'

# Настройки email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'  # Исправлено
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'konovalex@mail.ru'
EMAIL_HOST_PASSWORD = 'parol'
DEFAULT_FROM_EMAIL = 'konovalex@mail.ru'

# URL-адрес сайта
SITE_URL = 'http://localhost:8000'

from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = reverse_lazy('catalog:product_list')

# Настройки django_apscheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s A"  # Формат даты и времени
APSCHEDULER_RUN_NOW = True  # Запустить сразу же при старте приложения

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'mail': {  # Ваше приложение mail
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}