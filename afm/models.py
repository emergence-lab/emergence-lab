from django.db import models
import growths.models


class afm(models.Model):
    LOCATION_CHOICES = [
        ('c', 'Center'),
        ('r', 'Round'),
        ('f', 'Flat'),
    ]

    growth = models.ForeignKey(growths.models.growth)
    sample = models.ForeignKey(growths.models.sample)
    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3)
    zrange = models.DecimalField(max_digits=7, decimal_places=3)
    location = models.CharField(max_length=45, choices=LOCATION_CHOICES, default='c')
    size = models.DecimalField(max_digits=7, decimal_places=3)

    filename = models.CharField(max_length=150, blank=True)
    amplitude_filename = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '{0}_{1}_{2}.{3}'.format(self.growth, self.sample, self.location,
                                    str(self.scan_number).zfill(3))

    class Meta:
        db_table = 'afm'
