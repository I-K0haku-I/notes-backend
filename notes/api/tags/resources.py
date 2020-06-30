from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from middleware.masterkey import MasterKeyRequired
from notes.models import NoteTag

from .serializers import NoteTagSerializer


class NoteTagsViewSet(viewsets.ModelViewSet):
    queryset = NoteTag.objects.all()
    serializer_class = NoteTagSerializer

    def get_permissions(self):
        return [MasterKeyRequired()]
