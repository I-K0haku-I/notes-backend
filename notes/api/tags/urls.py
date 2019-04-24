from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .resources import NoteTagsViewSet

router = DefaultRouter()
router.register('notes', NoteTagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
