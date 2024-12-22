from .base import *

DEBUG = False
ALLOWED_HOSTS = ['wolfwilson.pythonanywhere.com']

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
