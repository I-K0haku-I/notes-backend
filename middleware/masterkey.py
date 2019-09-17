from django.conf import settings
from django.http import HttpResponseForbidden

class MasterKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        token = request.META.get('HTTP_COOL_TOKEN')
        if token is None:
            return HttpResponseForbidden('You need a cool token to access this.')
        if token != settings.VERY_COOL_PASSWORD:
            return HttpResponseForbidden('Your token was not cool enough.')
        response = self.get_response(request)
        return response