from datetime import date

from django_elasticsearch_dsl_drf.filter_backends import CompoundSearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from middleware.masterkey import MasterKeyRequired
from notes.documents import NoteDocument
from notes.models import Note, NoteTag
from notes.serializers import NoteDocumentSerializer

from .serializers import NotesSerializer


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def get_permissions(self):
        return [MasterKeyRequired()]

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = date.fromisoformat(str(start_date))
            end_date = date.fromisoformat(str(end_date))
            queryset = queryset.filter(time__date__range=[start_date, end_date])
        new_date = self.request.query_params.get('date')
        if new_date:
            # checking if date format would be useful, but works without it fine
            new_date = date.fromisoformat(str(new_date))
            queryset = queryset.filter(time__date=new_date)
        tags = self.request.query_params.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags)

        return queryset

# TODO: add filtering for timeframe too, only day possible right now


class NotesSearchViewSet(DocumentViewSet):
    document = NoteDocument
    serializer_class = NoteDocumentSerializer
    lookup_field = 'note_text'
    filter_backends = [CompoundSearchFilterBackend]
    search_fields = ('note_text',)
