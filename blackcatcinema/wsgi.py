"""
WSGI config for blackcatcinema project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Apuntar a la configuración de producción por defecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackcatcinema.settings.production')

application = get_wsgi_application()
