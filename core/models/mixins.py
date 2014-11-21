# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


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
class FunctionUIDMixin(models.Model):
    """
    Mixin for models that have a custom string uid.
    """
    uid = models.SlugField(max_length=25, blank=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid

    def _generate_uid(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(FunctionUIDMixin, self).save(*args, **kwargs)
        self.uid = self._generate_uid()
        super(FunctionUIDMixin, self).save(update_fields=['uid'])


class AutoUIDMixin(FunctionUIDMixin):
    """
    Mixin for models that have a string uid based on the objects primary key id.
    Uses the format prefix + zero-padded id + postfix.

    To override the default behavior, set the uid on instance creation. Any
    of the default elements may be used by inserting {prefix}, {id}, or
    {postfix} into the uid string. The approriate element will be substituted.
    """
    prefix = ''
    postfix = ''
    padding = 4

    class Meta:
        abstract = True

    def _generate_uid(self):
        uid = self.uid
        if uid == '':
            uid = '{prefix}{id}{postfix}'
        return uid.format(
            prefix=self.prefix,
            id=str(self.id).zfill(self.padding),
            postfix=self.postfix
        )
