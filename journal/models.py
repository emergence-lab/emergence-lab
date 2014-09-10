from __future__ import unicode_literals

from django.db import models

from actstream import registry
from autoslug import AutoSlugField
from markupfield.fields import MarkupField

import core.models


class journal_entry(models.Model):
    """
    Stores journal entries.
    """
    title = models.CharField(max_length=100)
    entry = MarkupField(blank=True, markup_type='markdown')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(core.models.operator)
    slug = AutoSlugField(populate_from='title', unique_with=('author'))
    investigations = models.ManyToManyField(core.models.investigation)

    class Meta:
        db_table = 'journal_entries'
