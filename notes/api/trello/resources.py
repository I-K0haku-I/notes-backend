
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response


class TrelloReceiverView(APIView):
    def get(self, request):
        return Response('BOOM')
        
