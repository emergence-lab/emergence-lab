from django.db import models
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage as labshare

import d180.models


def get_afm_path(instance, filename):
    return '/'.join(['growths' + instance.growth.growth_number[1],
                     instance.growth.growth_number, 'afm', filename])


class afm(models.Model):
    """
    Stores afm characterization information.
    """
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

    height = models.ImageField(upload_to=get_afm_path, storage=labshare,
                               max_length=150, blank=True, null=True)
    amplitude = models.ImageField(upload_to=get_afm_path, storage=labshare,
                                  max_length=150, blank=True, null=True)

    def __unicode__(self):
        return '{0}_{1}{2}_{3}.{4}'.format(self.growth.growth_number,
                                           self.sample.pocket, self.sample.piece,
                                           self.location, str(self.scan_number).zfill(3))

    def get_absolute_url(self):
        return reverse('afm_detail', args=(self.id, ))

    class Meta:
        db_table = 'afm'
        unique_together = ('growth', 'sample', 'scan_number', 'location')
