# Load base in order to then add/override with dev-only settings
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'd1d985bd-7d9e-4ef9-8850-064c8553578b'
if(os.path.exists(os.path.join(BASE_DIR, 'etc/key.txt'))):
    with open(os.path.join(BASE_DIR, 'etc/key.txt')) as f:
        SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

dbkey = ""
if(os.path.exists(os.path.join(BASE_DIR, 'etc/dbkey.txt'))):
    with open(os.path.join(BASE_DIR, 'etc/dbkey.txt')) as f:
        dbkey = f.read().strip()
DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rabbitloans',
        'USER': 'postgres',
        'PASSWORD': dbkey,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

    # 'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'etc/db.cnf'),
        # },
    # }
}
