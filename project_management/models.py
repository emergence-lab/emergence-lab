# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import autoslug

from core.models import ActiveStateMixin, TimestampMixin, fields
from core.models import Investigation


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                limit_choices_to={'is_active': True})

    class Meta:
        verbose_name = _('milestone')
        verbose_name_plural = _('milestones')

    def __str__(self):
        return self.name


class Literature(TimestampMixin, models.Model):
    """
    Scientific articles.
    """
    title = models.CharField(max_length=500)
    external_id = models.CharField(max_length=100, blank=True)
    abstract = fields.RichTextField(_('abstract'), blank=True, null=True)
    doi_number = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=4, blank=True)
    journal = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    investigations = models.ManyToManyField(Investigation,
                                        related_name='literature',
                                        related_query_name='literature',
                                        null=True)
    milestones = models.ManyToManyField(Milestone,
                                        related_name='literature',
                                        related_query_name='literature',
                                        null=True)


#
# class Keyword(models.Model):
#     name = models.CharField(max_length=45)
#     article = models.ManyToManyField(Literature,
#                                     related_name='keyword',
#                                     related_query_name='keyword',
#                                     null=True)
