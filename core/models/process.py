# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

from .mixins import TimestampMixin


class BaseProcess(TimestampMixin, models.Model):
    """
    Base class for all processes.
    """
    comment = models.TextField(blank=True)
    destructive = models.BooleanField(default=True)

    class Meta:
        abstract = True
