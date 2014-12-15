from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import time
from django.utils import timezone

from core.models import Investigation

from simulations.aws_simulations import ec2_metal_ops as metal

@python_2_unicode_compatible   
class Simulation(models.Model):
    
    def get_instance_types():
        m = metal.EC2_Connection(settings.AWS_EC2_REGION, settings.AWS_EC2_KEY, settings.AWS_EC2_SECRET)
        tmp = []
        for key in m.instance_detail_list().keys():
            desc = key.split('.')
            desc = str('{0} ({1})'.format(desc[1], desc[0]))
            tmp.append((key, desc))
        return tmp
    
    def is_completed(self):
        return self.finish_date is not None
    
    def elapsed_time(self):
        if self.start_date is None:
            return 0
        
        if self.finish_date is None:
            return timezone.now() - self.start_date
        
        return self.finish_date - self.start_date

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    investigations = models.ManyToManyField(Investigation)
    request_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    priority = models.BooleanField(default=False)
    execution_node = models.CharField(max_length=15, choices=get_instance_types())
    def __str__(self):              # __unicode__ on Python 2
        return '{0}, {1}, {2}'.format(str(self.user), str(self.completed), str(self.request_date))