from django_elasticsearch_dsl import Index, fields, Document
from elasticsearch_dsl import analyzer, token_filter

from notes.models import Note, NoteTag
from middleware.masterkey import db_local

note_index = Index('notes')
note_index.settings(number_of_shards=1, number_of_replicas=0)

# note_token_filter = token_filter('note_token_filter', type='stemmer', language='english')
edge15gram = token_filter('edge15gram', type='edge_ngram', min_gram=1, max_gram=15, preserver_original=True)

note_index_analyzer = analyzer(
    'note_index_analyzer',
    tokenizer='standard',
    filter=['lowercase', 'stop', 'snowball', edge15gram],
)
note_search_analyzer = analyzer(
    'note_index_analyzer',
    tokenizer='standard',
    filter=['lowercase', 'stop', 'snowball'],
)

@note_index.doc_type
class NoteDocument(Document):
    id = fields.IntegerField(attr='id')
    note_text = fields.Text(analyzer=note_index_analyzer, search_analyzer=note_search_analyzer, fields={'suggest': fields.Completion()})  # allows searching for detail and content at the same time
    detail = fields.TextField(attr='detail', analyzer=note_index_analyzer, search_analyzer=note_search_analyzer, copy_to='note_text', fields={'suggest': fields.Completion()})
    content = fields.TextField(attr='content', analyzer=note_index_analyzer, search_analyzer=note_search_analyzer, copy_to='note_text', fields={'suggest': fields.Completion()})
    time = fields.DateField(attr='time')

    class Django:
        model = Note
