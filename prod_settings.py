from oi_bus.base_settings import *
import os

try:
    with open('/var/lib/oi-bus/secret-key') as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    print('generating a secret key')
    import base64
    SECRET_KEY = base64.encodebytes(os.getrandom(32)).strip()
    with open('/var/lib/oi-bus/secret-key', 'w') as f:
        f.write(SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/oi-bus/db.sqlite3',
    },
}
TEAPOT = '/usr/share/oi-bus/memes'
STATIC_ROOT = '/var/lib/oi-bus/static'
MEDIA_ROOT = '/var/lib/oi-bus/files'

# to enable old-school self-registration, change to True
EVERYONE_IS_ADMIN = False

# when in trouble, you can uncomment this and set to True:
#
# DEBUG = False

# running an international competition?
# LANGUAGE_CODE = 'en'
