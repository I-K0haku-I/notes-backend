"""
WSGI config for k0haku project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from todo_app import create_app

django_app = get_wsgi_application()
flask_app = create_app()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = DispatcherMiddleware(flask_app, {'/b': django_app})

