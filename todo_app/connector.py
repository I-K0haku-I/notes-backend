from flask import g
from base_api_connector import GenericAPIConnector, APIResource
from django.conf import settings


class NotesBackendConnector(GenericAPIConnector):
    base_headers = {'cool-token': settings.VERY_COOL_PASSWORD}
    base_api_url = 'http://127.0.0.1:8000/b/api/'
    # base_api_url = 'https://me.k0haku.space/b/api/'
    notes = APIResource('all')
    tags = APIResource('all')


def get_conn():
    if 'conn' not in g:
        g.conn = NotesBackendConnector()
    return g.conn
