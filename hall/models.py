from __future__ import unicode_literals
from django.db import models
import growths.models


class hall(models.Model):
    """
    Stores hall characterization information.
    """
    growth = models.ForeignKey(growths.models.growth)
    sample = models.ForeignKey(growths.models.sample)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
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

    def __unicode__(self):
        return self.date

    class Meta:
        db_table = 'hall'
