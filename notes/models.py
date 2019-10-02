from datetime import timedelta

from django.db import models


class Note(models.Model):
    time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(seconds=0))
    content = models.TextField()
    detail = models.TextField(blank=True)
    tags = models.ManyToManyField('NoteTag', blank=True)
    is_done = models.BooleanField(default=False)



class NoteTag(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=6, default='000000')
