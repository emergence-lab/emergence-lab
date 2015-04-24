# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import uuid

from django.core.files.storage import default_storage as labshare
from django.conf import settings
from django.db import models

from mptt import models as mptt
import polymorphic

from core.models.mixins import TimestampMixin, UUIDMixin
from core.models import fields
from core.polymorphic import get_subclasses


def get_file_path(instance, filename):
    """
    Stores files in /process_data and generates a UUID-based file name
    """
    return '/'.join(['process_data',
                     uuid.uuid4().get_hex() + os.path.splitext(filename)[1]])


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
    legacy_identifier = models.SlugField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             limit_choices_to={'is_active': True})

    @staticmethod
    def get_process_class(slug):
        classes = get_subclasses(Process) + [Process]
        try:
            return next(p for p in classes if p.slug == slug)
        except StopIteration:
            raise ValueError('Process slug {} not valid'.format(slug))


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


class DataFile(polymorphic.PolymorphicModel, TimestampMixin):
    """
    Generic model for files associated with processes
    """
    partial_template = 'core/generic_file_partial.html'

    DATA_STATE = [
        ('raw', 'Raw'),
        ('cleaned', 'Cleaned'),
        ('extracted', 'Extracted'),
        ('analyzed', 'Analyzed'),
        ('other', 'Other')
    ]
    CONTENT_TYPE = [
        ('', 'Unknown'),
        ('application/octet-stream', 'Binary File'),
        ('application/pdf', 'PDF File'),
        ('application/vnd.ms-excel', 'Excel File'),
        ('application/vnd.openxmlformats-officedocument.spreadsheelml.sheet', 'Excel File'),
        ('image/png', 'PNG Image'),
        ('image/bmp', 'BMP Image'),
        ('image/jpeg', 'JPEG Image'),
        ('image/tiff', 'TIFF Image'),
        ('image/gif', 'GIF Image'),
        ('text/plain', 'Plaintext File'),
        ('text/csv', 'CSV File'),
    ]

    processes = models.ManyToManyField(Process,
                                       related_name='datafiles',
                                       related_query_name='datafiles')
    content_type = models.CharField(max_length=200, blank=True, choices=CONTENT_TYPE, default='')
    data = models.FileField(upload_to=get_file_path, storage=labshare,
                            max_length=200, blank=True, null=True)
    state = models.CharField(max_length=20, choices=DATA_STATE, default='raw')


class ProcessTemplate(TimestampMixin, models.Model):
    """
    Model for templating existing process details for later reference
    """
    process = models.ForeignKey(Process,
                                related_name='process',
                                related_query_name='process')
    name = models.CharField(max_length=50, blank=True)
    comment = fields.RichTextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                         limit_choices_to={'is_active': True})
