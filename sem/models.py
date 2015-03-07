# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.db import models
from django.core.files.storage import default_storage as labshare
from django.conf import settings

from core.models import Process


def get_file_path(instance, filename):
    """
    Stores sem scans in /:sample_uuid/:process_uuid/
    """
    return '/'.join(['process', instance.uuid, filename])
    #return filename


class SEMScan(Process):
    """
    Stores SEM characterization images.
    """
    name = 'SEM Image'
    slug = 'sem'
    is_destructive = False

    TOOL_CHOICES = [
        ('leo1550', 'LEO 1550'),
        ('esem_600', 'FEI eSEM'),
        ('fib_1200', 'FEI Dual-Beam FIB'),
    ]

    image_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to=get_file_path, storage=labshare, max_length=150, blank=True, null=True)
    #image = models.ImageField(max_length=150, blank=True, null=True)

    magnification = models.FloatField(blank=True, null=True)
    image_source = models.CharField(max_length=45, choices=TOOL_CHOICES, default='esem_600')
