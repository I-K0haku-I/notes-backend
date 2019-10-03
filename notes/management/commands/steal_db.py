from settings_local import VERY_COOL_PASSWORD  # command local only anyway
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_duration

from base_api_connector import GenericAPIConnector, APIResource

from notes.models import Note, NoteTag


class Connector(GenericAPIConnector):
    base_api_url = 'https://www.k0haku.space/b/api/'
    base_headers = {'cool-token': VERY_COOL_PASSWORD}
    notes = APIResource('all')
    tags = APIResource('all')


c = Connector()


class Command(BaseCommand):
    def handle(self, *args, **options):
        tags = c.tags.list().json()
        NoteTag.objects.all().delete()
        tags_objs = tuple(NoteTag(**t) for t in tags)
        NoteTag.objects.bulk_create(tags_objs)

        notes = c.notes.list().json()
        Note.objects.all().delete()
        with transaction.atomic():
            for n in notes:
                tags = n.pop('tags', None)
                duration = n.pop('duration', None)
                note = Note(duration=parse_duration(duration), **n)
                note.save()
                note.tags.set(tags)
                note.save()
