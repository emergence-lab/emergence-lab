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
    slug = 'split-sample'
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
