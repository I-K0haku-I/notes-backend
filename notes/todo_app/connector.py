from flask import g
from base_api_connector import GenericAPIConnector, APIResource


class NotesBackendConnector(GenericAPIConnector):
    base_headers = {'cool-token': 'hmmmmm'}
    base_api_url = 'https://me.k0haku.space/b/api/'
    notes = APIResource('all')
    tags = APIResource('all')


def get_conn():
    if 'conn' not in g:
        g.conn = NotesBackendConnector()
    return g.conn
