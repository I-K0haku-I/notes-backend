from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from notes.models import NoteTag

from .serializers import NoteTagSerializer

class NoteTagsViewSet(viewsets.ModelViewSet):
    queryset = NoteTag.objects.all()
    serializer_class = NoteTagSerializer 
