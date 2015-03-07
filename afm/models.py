# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.core.files.storage import default_storage as labshare

from core.models import Process


def get_afm_path(instance, filename):
    """
    Stores afm scans in /:sample_uuid/:afm_uuid/
    """
    return '/'.join(['process', instance.uuid, filename])


class AFMScan(Process):
    """
    Stores afm characterization information.
    """
    name = 'AFM Scan'
    slug = 'afm'
    is_destructive = False

    LOCATION_CHOICES = [
        ('c', 'Center'),
        ('r', 'Round'),
        ('f', 'Flat'),
    ]

    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3)
    zrange = models.DecimalField(max_digits=7, decimal_places=3)
    location = models.CharField(max_length=45, choices=LOCATION_CHOICES, default='c')
    size = models.DecimalField(max_digits=7, decimal_places=3)

    height = models.ImageField(upload_to=get_afm_path, storage=labshare,
                               max_length=150, blank=True, null=True)
    amplitude = models.ImageField(upload_to=get_afm_path, storage=labshare,
                                  max_length=150, blank=True, null=True)
