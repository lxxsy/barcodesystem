"""
Django settings for BarcodeSystem project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
# sys.path.insert(0, os.path.join(BASE_DIR, 'static'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%yg&0164t4%#34!q3-4vbhn647j=*&)w^asujo^3sscfm%!r7+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
# 应用注册中心
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'bc_formula',
    'bc_rmaterial',
    'bc_product',
    'bc_production',
    'bc_test',
    'bc_backstage',
    'bc_batchingrecord',
    'bc_special',
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

ROOT_URLCONF = 'BarcodeSystem.urls'
# 模板文件夹配置中心
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'static')],
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

WSGI_APPLICATION = 'BarcodeSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# 数据库配置中心
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'barcodesystem',
        'USER': 'postgres',
        'PASSWORD': '941128',
        'HOST': "localhost",
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # True改为False, 否则Django存储数据库内容时, 会使用UTC时间.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# 设置静态资源的访问路径
STATIC_URL = '/static/'
# 设置静态资源的存储路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = '/var/www/BarcodeSystem/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# 创建日志保存文件
# LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址文件不存在，则自动创建

# LOGGING = {
#  'version': 1,  # 指明dictConnfig的版本，目前就只有一个版本
#  'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置,选择否就好
# }






























