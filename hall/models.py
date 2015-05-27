# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from core.models import DataFile


class HallData(DataFile):
    """
    Stores data for an instance of a Hall process.
    """
    temperature = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=300.0)
    symmetry_factor = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=1.0)
    sheet_coefficient = models.FloatField(blank=True, null=True)
    sheet_resistance = models.FloatField(blank=True, null=True)
    sheet_concentration = models.FloatField(blank=True, null=True)
    thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    mobility = models.FloatField(blank=True, null=True)
    bulk_coefficient = models.FloatField(blank=True, null=True)
    bulk_resistance = models.FloatField(blank=True, null=True)
    bulk_concentration = models.FloatField(blank=True, null=True)
