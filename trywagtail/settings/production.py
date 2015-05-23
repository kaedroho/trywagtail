import os

from .base import *


env = os.environ.copy()


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['trywagtail.kaed.uk']


if 'DJANGO_SECRET_KEY' in env:
    SECRET_KEY = env['DJANGO_SECRET_KEY']


try:
    from .local import *
except ImportError:
    pass
