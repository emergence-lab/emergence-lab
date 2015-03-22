# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.core.files.storage import default_storage as labshare

from core.models import Process


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

    image_source = models.CharField(max_length=45,
                                    choices=TOOL_CHOICES,
                                    default='esem_600',
                                    blank=True,
                                    null=True)
