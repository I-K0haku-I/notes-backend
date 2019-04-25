from rest_framework import serializers

from notes.models import Note

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
