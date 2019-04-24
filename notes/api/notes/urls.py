from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .resources import NotesViewSet

router = DefaultRouter()
router.register('notes', NotesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
