# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import autoslug

from .mixins import ActiveStateMixin, TimestampMixin
from .user import User
from . import fields


@python_2_unicode_compatible
class Project(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information on a project, which is a higher level organizational
    tool.
    """
    name = models.CharField(_('name'), max_length=45)
    slug = autoslug.AutoSlugField(_('slug'), populate_from='name')
    description = fields.RichTextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Investigation(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information on an individual investigation related to one or more
    projects.
    """
    name = models.CharField(_('name'), max_length=45)
    slug = autoslug.AutoSlugField(_('slug'), populate_from='name')
    description = fields.RichTextField(_('description'), blank=True)
    project = models.ForeignKey(Project, verbose_name=_('project'))

    class Meta:
        verbose_name = _('investigation')
        verbose_name_plural = _('investigations')

    def __str__(self):
        return self.name


class ProjectTracking(models.Model):
    """
    Stores ownership and tracking information for projects.
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    is_owner = models.BooleanField(default=False)