# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin, AutoUIDMixin, FunctionUIDMixin
from core import fields


class Process(polymorphic.PolymorphicModel, AutoUIDMixin, TimestampMixin):
    """
    Base class for all processes.
    """
    prefix = 'proc-'
    name = 'Generic Procss'
    slug = 'generic-process'
    is_destructive = True

    comment = fields.RichTextField(blank=True)


class SplitProcess(Process):
    prefix = 'split-'
    name = 'Split Sample'
    slug = 'split-sample'
    is_destructive = False


class ProcessNode(mptt.MPTTModel, FunctionUIDMixin, TimestampMixin):
    """
    Model representing the nodes in a tree of various processes done to
    a sample.
    """
    comment = fields.RichTextField(blank=True)
    parent = mptt.TreeForeignKey('self', null=True, related_name='children')
    process = models.ForeignKey(Process)
    piece = models.CharField(max_length=5)

    def _generate_uid(self):
        return '{0}_{1}.{2}'.format(self.get_root().sample.uid, self.piece,
                                    self.process.uid)
