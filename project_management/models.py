# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from core.models import TimestampMixin, fields, Milestone, Investigation


class Literature(TimestampMixin, models.Model):
    """
    Scientific articles.
    """
    title = models.CharField(max_length=500)
    external_id = models.CharField(max_length=100, blank=True)
    abstract = fields.RichTextField(_('abstract'), blank=True, null=True)
    doi_number = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    journal = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    investigations = models.ManyToManyField(Investigation,
                                        related_name='literature',
                                        related_query_name='literature')
    milestones = models.ManyToManyField(Milestone,
                                        related_name='literature',
                                        related_query_name='literature')
