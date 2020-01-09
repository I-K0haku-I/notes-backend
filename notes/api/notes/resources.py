from datetime import date

from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from notes.models import Note, NoteTag

from .serializers import NotesSerializer

class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

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
