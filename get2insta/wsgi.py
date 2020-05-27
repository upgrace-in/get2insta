"""
WSGI config for get2insta project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'get2insta.settings')

# application = get_wsgi_application()

application = get_wsgi_application()
application = WhiteNoise(application, root='static')
application.add_files('staticfiles')
