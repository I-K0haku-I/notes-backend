from django.db import models


class Note(models.Model):
    content = models.TextField()
    types = models.ManyToManyField('NoteType')
    tags = models.ManyToManyField('NoteTag')


class NoteType(models.Model):
    name = models.CharField(max_length=15)


class NoteTag(models.Model):
    name = models.CharField(max_length=15)