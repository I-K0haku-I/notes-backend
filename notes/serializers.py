from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from notes.documents import NoteDocument


class NoteDocumentSerializer(DocumentSerializer):
    class Meta:
        document = NoteDocument
        fields = (
            'id',
            'detail',
            'content',
            'time',
            'note_text',
        )
