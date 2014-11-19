# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin
from core import fields


@python_2_unicode_compatible
class Process(polymorphic.PolymorphicModel, TimestampMixin):
    """
    Base class for all processes.
    """
    uid = models.SlugField(max_length=25)
    comment = fields.RichTextField(blank=True)

    def __str__(self):
        return self.uid


@python_2_unicode_compatible
class ProcessNode(mptt.MPTTModel, TimestampMixin):
    """
    Model representing the nodes in a tree of various processes done to
    a sample.
    """
    comment = fields.RichTextField(blank=True)
    parent = mptt.TreeForeignKey('self', null=True, related_name='children')
    process = models.OneToOneField(Process)

    def __str__(self):
        return self.process.__str__()
