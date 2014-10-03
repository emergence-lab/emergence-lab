from __future__ import unicode_literals

from django.db import models

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

import core.models


class journal_entry(models.Model):
    """
    Stores journal entries.
    """
    title = models.CharField(max_length=100)
    entry = RichTextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(core.models.operator)
    slug = AutoSlugField(populate_from='title', unique_with=('author'))
    investigations = models.ManyToManyField(core.models.Investigation)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'journal_entries'
