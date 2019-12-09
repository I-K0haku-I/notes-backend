from threading import local
from django.conf import settings
from django.http import HttpResponseForbidden

db_local = local()

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
    def db_for_read(self, model, **hints):
        return db_local.db_to_use
    
    def db_for_write(self, model, **hints):
        return db_local.db_to_use