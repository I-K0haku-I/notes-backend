from types import SimpleNamespace
from django.core.management.base import BaseCommand
from django.db import transaction
from notes.models import Note, NoteType, NoteTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        notes = Note.objects.all().values_list('id', 'type__name', named=True)
        notes = [SimpleNamespace(tag=None, id=n.id, type=n.type__name) for n in notes]
    
        tags_id = list(NoteTag.objects.all().values_list('id', flat=True))
        tags_name = list(NoteTag.objects.all().values_list('name', flat=True))
        for n in notes:
            if n.type in tags_name:
                new_tag_id = tags_id[tags_name.index(n.type)]
            else:
                new_tag = NoteTag(name=n.type)
                new_tag.save()
                tags_id.append(new_tag.id)
                tags_name.append(new_tag.name)
                new_tag_id = new_tag.id
            n.type = None
            n.tag = new_tag_id

        # makes it so query gets execute at the end of context manager
        with transaction.atomic():
            notes_r = Note.objects.all()
            for i, n in enumerate(notes_r):
                n.type = None
                n.tags.add(notes[i].tag)
                n.save()
        
        