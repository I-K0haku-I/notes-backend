from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from notes.models import NoteType

from .serializers import NoteTypeSerializer

class NoteTypesViewSet(viewsets.ModelViewSet):
    queryset = NoteType.objects.all()
    serializer_class = NoteTypeSerializer
