from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .resources import NoteTypesViewSet

router = DefaultRouter()
router.register('notes', NoteTypesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
