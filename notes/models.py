from django.db import models


class Note(models.Model):
    time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    detail = models.TextField()
    types = models.ManyToManyField('NoteType', blank=True)
    tags = models.ManyToManyField('NoteTag', blank=True)


class NoteType(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True)


class NoteTag(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=6)