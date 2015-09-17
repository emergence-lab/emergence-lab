# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import autoslug

from .mixins import ActiveStateMixin, TimestampMixin, AccessControlShortcutMixin
from .user import User
from . import fields


@python_2_unicode_compatible
class Project(AccessControlShortcutMixin, ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information on a project, which is a higher level organizational
    tool.
    """
    name = models.CharField(_('name'), max_length=45)
    slug = autoslug.AutoSlugField(_('slug'), populate_from='name')
    description = fields.RichTextField(_('description'), blank=True)
    owner_group = models.ForeignKey(Group, verbose_name=_('owner_group'),
                                    related_name='+', blank=True, null=True)
    member_group = models.ForeignKey(Group, verbose_name=_('member_group'),
                                    related_name='+', blank=True, null=True)
    viewer_group = models.ForeignKey(Group, verbose_name=_('viewer_group'),
                                    related_name='+', blank=True, null=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Investigation(AccessControlShortcutMixin, ActiveStateMixin, TimestampMixin, models.Model):
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

    @property
    def owner_group(self):
        return self.project.owner_group

    @property
    def member_group(self):
        return self.project.member_group

    @property
    def viewer_group(self):
        return self.project.viewer_group

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Milestone(AccessControlShortcutMixin, ActiveStateMixin, TimestampMixin, models.Model):
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

    @property
    def owner_group(self):
        return self.investigation.owner_group

    @property
    def member_group(self):
        return self.investigation.member_group

    @property
    def viewer_group(self):
        return self.investigation.viewer_group

    def __str__(self):
        return self.name


class MilestoneNote(AccessControlShortcutMixin, TimestampMixin, models.Model):
    """
    Stores a note attached to a milestone object
    """
    note = fields.RichTextField(_('note'), blank=True)
    milestone = models.ForeignKey(Milestone,
                                related_name='note',
                                related_query_name='note',
                                null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                limit_choices_to={'is_active': True})

    @property
    def owner_group(self):
        return self.milestone.owner_group

    @property
    def member_group(self):
        return self.milestone.member_group

    @property
    def viewer_group(self):
        return self.milestone.viewer_group


class Task(AccessControlShortcutMixin, ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores a task with potential relation to a milestone.
    """
    description = fields.RichTextField(_('description'), blank=True)
    due_date = models.DateField()
    milestone = models.ForeignKey(Milestone,
                                related_name='task',
                                related_query_name='task',
                                null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                limit_choices_to={'is_active': True})

    @property
    def owner_group(self):
        return self.milestone.owner_group

    @property
    def member_group(self):
        return self.milestone.member_group

    @property
    def viewer_group(self):
        return self.milestone.viewer_group


class ProjectTracking(models.Model):
    """
    Stores ownership and tracking information for projects.
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    is_owner = models.BooleanField(default=False)


@receiver(models.signals.post_save, sender=Project)
def create_project_groups(sender, instance=None, created=False, **kwargs):
    if created:
        owner = Group.objects.create(name='rbac_project_owner_{}'.format(instance.slug))
        member = Group.objects.create(name='rbac_project_member_{}'.format(instance.slug))
        viewer = Group.objects.create(name='rbac_project_viewer_{}'.format(instance.slug))
        instance.owner_group = owner
        instance.member_group = member
        instance.viewer_group = viewer
        instance.save()
