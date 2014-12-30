# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin, UUIDMixin
from core import fields


class Process(polymorphic.PolymorphicModel, UUIDMixin, TimestampMixin):
    """
    Base class for all processes. A process represents anything done to a
    sample which results in data (numerical or visual) or alters the properties
    of the sample.

    name: The human readable name for the process
    slug: The computer-consumed identifier to tell which type of process the
          instance is. Used to help identify which fields are availiable.
    is_destructive: Boolean that identifies whether the process is destructive,
                    meaning that the sample is altered in some way and that
                    repeating past processes may give different results.
    """
    prefix = 'p'

    name = 'Generic Process'
    slug = 'generic-process'
    is_destructive = True

    comment = fields.RichTextField(blank=True)


class SplitProcess(Process):
    """
    Process representing splitting a sample into multiple parts or pieces.
    """
    name = 'Split Sample'
    slug = 'split-process'
    is_destructive = False


class ProcessNode(mptt.MPTTModel, UUIDMixin, TimestampMixin):
    """
    Model representing the nodes in a tree of various processes done to
    a sample.
    """
    prefix = 'n'

    comment = fields.RichTextField(blank=True)
    parent = mptt.TreeForeignKey('self', null=True, related_name='children')
    process = models.ForeignKey(Process, null=True)
    piece = models.CharField(max_length=5)
