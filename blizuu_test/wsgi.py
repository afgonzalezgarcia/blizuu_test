"""
WSGI config for blizuu_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

application = get_wsgi_application()
