# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from autoslug import AutoSlugField

from core.models import Investigation, TimestampMixin, User
from core.models.fields import RichTextField


@python_2_unicode_compatible
class JournalEntry(TimestampMixin, models.Model):
    """
    Stores journal entries.
    """
    title = models.CharField(max_length=100)
    entry = RichTextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = AutoSlugField(populate_from='title', unique_with=('author'))
    investigations = models.ManyToManyField(Investigation)

    def __str__(self):
        return self.title
