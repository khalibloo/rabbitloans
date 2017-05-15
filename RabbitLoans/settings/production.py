# Load base in order to then add/override with production-only settings
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', 'localhost']
SECRET_KEY = os.environ["SECRET_KEY"]

dbkey = os.environ["DB_KEY"]
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
# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# TEMPLATES = [{
    # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
    # 'OPTIONS': {
        # 'loaders': [
            # ('django.template.loaders.cached.Loader', [
                # 'django.template.loaders.filesystem.Loader',
                # 'django.template.loaders.app_directories.Loader',
            # ]),
        # ],
    # },
# }]

#Security options
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
#CONN_MAX_AGE = [time]

#Production email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'khali@ratrace.com'
# with open(os.path.join(BASE_DIR, 'etc/emailkey.txt')) as f:
    # EMAIL_HOST_PASSWORD = f.read().strip()
# MAIL_USE_TLS = True


EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
    
DEFAULT_FROMEMAIL = 'studycalabash@gmail.com' #for regular emails sent to users
SERVER_EMAIL = 'root@localhost' #for server errors sent to admin

