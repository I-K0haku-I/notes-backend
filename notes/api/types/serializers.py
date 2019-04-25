from rest_framework import serializers

from notes.models import NoteType

class NoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteType
        fields = '__all__'
