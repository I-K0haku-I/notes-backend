from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .notes.resources import NotesViewSet
from .tags.resources import NoteTagsViewSet


router = DefaultRouter()
router.register('notes', NotesViewSet)
router.register('tags', NoteTagsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
