from .base_settings import *
import os

try:
    with open('/var/db/oi-bus/secret-key') as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    print('generating a secret key')
    import base64
    SECRET_KEY = base64.encodebytes(os.getrandom(32)).strip()
    with open('/var/db/oi-bus/secret-key', 'w') as f:
        f.write(SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/db/oi-bus/db.sqlite3',
    },
}
TEAPOT = '/usr/share/oi-bus/memes'
STATIC_ROOT = '/var/run/oi-bus/static'
MEDIA_ROOT = '/var/db/oi-bus/files'
EVERYONE_IS_ADMIN = os.getenv('EVERYONE_IS_ADMIN', 'OVER_MY_DEAD_BODY') == 'AND_I_ACCEPT_THE_CONSEQUENCES'

# when in trouble, you can uncomment this and set to True:
#
# DEBUG = False

# running an international competition?
# LANGUAGE_CODE = 'en'
