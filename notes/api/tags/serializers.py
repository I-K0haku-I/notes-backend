from rest_framework import serializers

from notes.models import NoteTag

class NoteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = (
            'id',
            'name',
        )
