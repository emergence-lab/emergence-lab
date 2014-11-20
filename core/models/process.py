# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin, UIDMixin
from core import fields


class Process(polymorphic.PolymorphicModel, UIDMixin, TimestampMixin):
    """
    Base class for all processes.
    """
    prefix = 'proc-'

    comment = fields.RichTextField(blank=True)


@python_2_unicode_compatible
class ProcessNode(mptt.MPTTModel, TimestampMixin):
    """
    Model representing the nodes in a tree of various processes done to
    a sample.
    """
    comment = fields.RichTextField(blank=True)
    parent = mptt.TreeForeignKey('self', null=True, related_name='children')
    process = models.ForeignKey(Process)
    piece = models.CharField(max_length=5)

    def __str__(self):
        return '{0}_{1}'.format(self.get_root().sample.uid, self.piece)
