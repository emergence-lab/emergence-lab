# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import six

from core import fields


class ActiveStateManager(models.Manager):
    """
    Manager to filter on the ``active`` field.
    """
    def __init__(self, active_test):
        super(ActiveStateManager, self).__init__()
        self.active_test = active_test

    def get_queryset(self):
        return (super(ActiveStateManager, self)
                    .get_queryset().filter(is_active=self.active_test))


class ActiveStateMixin(models.Model):
    """
    Mixin for models that keep an active/inactive state.
    """
    is_active = models.BooleanField(_('active'), default=True)
    status_changed = models.DateTimeField(_('status changed'), null=True,
                                          blank=True, editable=False)

    objects = models.Manager()
    active_objects = ActiveStateManager(active_test=True)
    inactive_objects = ActiveStateManager(active_test=False)

    class Meta:
        abstract = True

    def activate(self, save=True):
        """
        Activate the object, raise an exception if it was already active.
        """
        if self.is_active:
            raise Exception('{0} was already active'.format(self._meta.verbose_name))
        self.is_active = True
        self.status_changed = timezone.now()
        if save:
            self.save()

    def deactivate(self, save=True):
        """
        Deactivate the object, raise an exception if it was already active.
        """
        if not self.is_active:
            raise Exception('{0} was already not active'.format(self._meta.verbose_name))
        self.is_active = False
        self.status_changed = timezone.now()
        if save:
            self.save()


class TimestampMixin(models.Model):
    """
    Mixin for models that keeps track of when an object was created or modified.
    """
    created = models.DateTimeField(_('date created'), auto_now_add=True)
    modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AutoUUIDMixin(models.Model):
    prefix = ''
    padding = 4

    class Meta:
        abstract = True

    def __str__(self):
        return self.uuid

    @property
    def uuid(self):
        return '{prefix}{uuid}'.format(prefix=self.prefix,
                                       uuid=str(self.pk).zfill(self.padding))

    @classmethod
    def strip_uuid(cls, uuid):
        return int(uuid[len(cls.prefix):])


@python_2_unicode_compatible
class UUIDMixin(models.Model):
    """
    Mixin for models that have a long random uuid and a short form meant
    for human consumption.
    """
    short_length = 7
    prefix = ''

    uuid_full = fields.UUIDField(version=4, auto=True, hyphenate=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.uuid

    @property
    def uuid(self):
        return '{prefix}{uuid}'.format(
            prefix=self.prefix, uuid=self.uuid_full.hex[:self.short_length])

    @classmethod
    def strip_uuid(cls, uuid):
        if not isinstance(uuid, six.string_types):
            return uuid.hex
        return uuid[len(cls.prefix):]
