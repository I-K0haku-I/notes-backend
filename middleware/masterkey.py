from threading import local
from django.conf import settings
from django.http import HttpResponseForbidden
from flask import has_app_context, session

db_local = local()
db_local.db_to_use = 'default'

class MasterKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        token = request.META.get('HTTP_COOL_TOKEN')
        if token is None:
            return HttpResponseForbidden('You need a cool token to access this.')
        if token == settings.VERY_COOL_PASSWORD:
            # return HttpResponseForbidden('Your token was not cool enough.')
            db_local.db_to_use = 'private'
        else:
            db_local.db_to_use = 'default'
        response = self.get_response(request)
        return response


class MasterKeyDBRouter:
    def get_access(self):
        if hasattr(db_local, 'db_to_use'):
            return db_local.db_to_use
        elif has_app_context():
            if session['is_logged_in']:
                return 'private'
        return 'default'

    def db_for_read(self, model, **hints):
        return self.get_access()

    def db_for_write(self, model, **hints):
        return self.get_access()