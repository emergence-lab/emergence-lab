# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import uuid

from django.db import models
from django.core.files.storage import default_storage as labshare

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin, UUIDMixin
from . import fields


def get_file_path(instance, filename):
    """
    Stores files in /process/:process_uuid/filename/
    """
    return '/'.join(['process', uuid.uuid4().get_hex() + os.path.splitext(filename)[1]])


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

    def get_sample(self):
        return self.get_root().sample


class DataFile(models.Model):
    """
    Generic model for files associated with processes
    """
    processes = models.ManyToManyField(Process,
                                       related_name='datafiles',
                                       related_query_name='datafiles')
    content_type = models.CharField(max_length=10, null=True, blank=True)
    data = models.FileField(upload_to=get_file_path, storage=labshare,
                            max_length=200, blank=True, null=True)
