
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

import logging

logger = logging.getLogger('trello')

class TrelloReceiverView(APIView):
    def get(self, request):
        logger.error('####: ' + str(request.data))
        return Response('BOOM')
        
