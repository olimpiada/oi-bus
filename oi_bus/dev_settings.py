from .base_settings import *
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "doesn't really matter to me"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
TEAPOT = os.path.join(BASE_DIR, 'memes')
MEDIA_ROOT = os.path.join(BASE_DIR, 'dev_media')
EVERYONE_IS_ADMIN = os.getenv('EVERYONE_IS_ADMIN', '') == 'TRUE'
EVERYONE_IS_ADMIN = os.getenv('EVERYONE_IS_ADMIN', 'OVER_MY_DEAD_BODY') == 'AND_I_ACCEPT_THE_CONSEQUENCES'

# when in trouble, you can uncomment this and set to True:
#
# DEBUG = False
