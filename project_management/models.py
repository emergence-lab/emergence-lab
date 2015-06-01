# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import autoslug

from core.models import ActiveStateMixin, TimestampMixin, fields
from core.models import Investigation, Process, DataFile



class Milestone(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information related to short-term project goals.
    """
    due_date = models.DateField()
    name = models.CharField(_('name'), max_length=45)
    slug = autoslug.AutoSlugField(_('slug'), populate_from='name')
    description = fields.RichTextField(_('description'), blank=True)
    investigation = models.ForeignKey(Investigation,
                                related_name='milestone',
                                related_query_name='milestone',
                                null=True)


class ProgressUpdate(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Records updates to a milestone based on project activity.
    """
    process = models.ForeignKey(Process,
                                related_name='progress',
                                related_query_name='progress',
                                null=True)
    datafile = models.ForeignKey(DataFile,
                                related_name='progress',
                                related_query_name='progress',
                                null=True)
    description = fields.RichTextField(_('description'), blank=True)
    milestone = models.ManyToManyField(Milestone,
                                related_name='progress',
                                related_query_name='progress',)


class Literature(TimestampMixin, models.Model):
    """
    Scientific articles.
    """
    title = models.CharField(max_length=500)
    external_id = models.CharField(max_length=100)
    abstract = fields.RichTextField(_('abstract'), blank=True)
    doi_number = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

#
# class Keyword(models.Model):
#     name = models.CharField(max_length=45)
#     article = models.ManyToManyField(Literature,
#                                     related_name='keyword',
#                                     related_query_name='keyword',
#                                     null=True)
