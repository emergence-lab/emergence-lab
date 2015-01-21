# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from core.models import mixins
from core.models import Process


class ParentProcess(Process):
    """
    Test-only model to test single-level inheritance with additional fields.
    """
    parent_field = models.IntegerField()


class ChildProcess(ParentProcess):
    """
    Test-only model to test multiple-level inheritance with additional fields.
    """
    child_field = models.IntegerField()


class ActiveStateModel(mixins.ActiveStateMixin, models.Model):
    """
    Test-only model to test ActiveStateMixin.
    """
    pass


class UUIDModel(mixins.UUIDMixin, models.Model):
    """
    Test-only model to test UUIDMixin.
    """
    short_length = 10
    prefix = 'prefix'


class AutoUUIDModel(mixins.AutoUUIDMixin, models.Model):
    """
    Test-only model to test AutoUUIDMixin.
    """
    prefix = 'prefix'
    padding = 6
