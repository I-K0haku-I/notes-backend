from datetime import date

from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from notes.models import Note

from .serializers import NotesSerializer

class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        new_date = self.request.query_params.get('date')
        if new_date is not None:
            new_date = date.fromisoformat(str(new_date))
            queryset = queryset.filter(time__date=new_date)
        return queryset

# TODO: add filtering for timeframe too, only day possible right now
