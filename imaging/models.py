# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.core.files.storage import default_storage as labshare

from core.models import Process


def get_file_path(instance, filename):
    """
    Stores afm scans in /:sample_uuid/:process_uuid/
    """
    return '/'.join(['growths' + instance.sample.uuid, instance.uuid, filename])

class SEM(Process):
    """
    Stores SEM characterization images.
    """
    name = 'SEM Image'
    slug = 'sem'
    is_destructive = False

    TOOL_CHOICES = [
        ('leo1550', 'LEO 1550'),
        ('esem_600', 'FEI sSEM'),
        ('fib_1200', 'FEI Dual-Beam FIB'),
    ]

    image_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to=get_file_path, storage=labshare,
                               max_length=150, blank=True, null=True)
    magnification = models.FloatField(blank=True, null=True)
    image_source = models.CharField(max_length=45, choices=TOOL_CHOICES, default='esem_600')

class OpticalImage(Process):
    """
    Stores optical characterization images.
    """
    name = 'Optical Image'
    slug = 'optical'
    is_destructive = False

    image_number = models.IntegerField(defailt=0)
    image = models.ImageField(upload_to=get_file_path, storage=labshare,
                              max_length=150, blank=True, null=True)
    magnification = models.FloatField(blank=True, null=True)
    
