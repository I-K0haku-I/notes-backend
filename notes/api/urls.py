from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .notes.resources import NotesViewSet
from .tags.resources import NoteTagsViewSet
from .trello.resources import TrelloReceiverView


router = DefaultRouter()
router.register('notes', NotesViewSet)
router.register('tags', NoteTagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trello/', TrelloReceiverView.as_view(), name='trello')
]
