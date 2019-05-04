from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from notes.models import Note

from .serializers import NotesSerializer

class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

# TODO: add filtering for timeframes, through params?
