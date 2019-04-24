from django.urls import path, include

urlpatterns = [
    path('notes/', include('notes.api.notes.urls')),
    path('tags/', include('notes.api.tags.urls')),
    path('types/', include('notes.api.types.urls')),
]
