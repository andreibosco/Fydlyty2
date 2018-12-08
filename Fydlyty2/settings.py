"""
Django settings for Fydlyty2 project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sdd!r4o2u5s-o!dwo11ml9u==7w(rrd2@=qw#fkc^sb$ww!y)2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#AUTH_PROFILE_MODULE = 'accounts.userprofile'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Fydlyty2.accounts',
    'Fydlyty2.game',

    'sorl.thumbnail',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Fydlyty2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "Fydlyty2", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'Fydlyty2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fydlyty',
        'USER': 'test',
        'PASSWORD': 'test',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "Fydlyty2", "static"),
)

TEMP_SCRIPT = os.path.join(BASE_DIR, "Fydlyty2", "static", "files", "dialogue_script.csv")

LANGUAGE = {
    'Good morning': ['Good afternoon', 'Good evening', 'Good night'],
    'Good evening': ['Good morning', 'Good afternoon', 'Good night'],
    'Good night': ['Good morning', 'Good afternoon', 'Good evening'],
    'Mr.': ['Miss', 'Ms.', 'Mrs.'],
    'Mrs.': ['Miss', 'Ms.', 'Mr.'],
    'Miss': ['Mr.', 'Ms.', 'Mrs.'],
    'Ms.': ['Miss', 'Mrs.', 'Mr.'],
}

HELP = {
    'N': ['Good Work! Build upon your efforts.', 'You have started to understand this game really well.', 'Bravo!'],
    'M': ['Oh no! They didn\'t like it.', 'Don\'t repeat this mistake again.', 'They got upset. Try not to repeat this mistake again'],
    'A': ['This is serious! You have to be careful',],
}
