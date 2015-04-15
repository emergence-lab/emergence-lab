# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from core.models import DataFile, Process


class AFMScan(Process):
    """
    Stores afm characterization information.
    """
    name = 'AFM Scan'
    slug = 'afm'
    is_destructive = False


class AFMFile(DataFile):
    """
    Stores the raw file and extracted data associated with an afm scan.
    """
    partial_template = 'afm/afm_detail_partial.html'

    LOCATION_CHOICES = [
        ('c', 'Center'),
        ('r', 'Round'),
        ('f', 'Flat'),
    ]
    IMAGE_TYPE = [
        ('Raw', 'Raw'),
        ('Height', 'Height'),
        ('Amplitude', 'Amplitude'),
        ('Phase', 'Phase'),
    ]

    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3)
    zrange = models.DecimalField(max_digits=7, decimal_places=3)
    location = models.CharField(max_length=45, choices=LOCATION_CHOICES, default='c')
    image_type = models.CharField(max_length=45, choices=IMAGE_TYPE, default='Height')
    size = models.DecimalField(max_digits=7, decimal_places=3)
