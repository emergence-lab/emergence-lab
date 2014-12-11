from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import time

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
    
    user = models.ForeignKey(User)
    request_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    priority = models.BooleanField(default=False)
    execution_node = models.CharField(max_length=15, choices=get_instance_types())
    completed = models.BooleanField(default=False)
    input_file_path = models.CharField(max_length=500, blank=True)
    output_file_path = models.CharField(max_length=500, blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return '{0}, {1}, {2}'.format(str(self.user), str(self.completed), str(self.request_date))