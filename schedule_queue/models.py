from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import time

import schedule_queue.config as tools

from growths.models import Platter

#class Tool(models.Model):
#    tool_name = models.CharField(max_length=20)
#    max_reservations = models.IntegerField(default=0)
#    def __str__(self):              # __unicode__ on Python 2
#        return self.tool_name
    
#class Platter(models.Model):
#    platter_name = models.CharField(max_length=20)
#    start_date = models.DateField()
#    tool = models.ForeignKey(Tool)
#    def __str__(self):              # __unicode__ on Python 2
#        return self.platter_name
    
@python_2_unicode_compatible    
class Reservation(models.Model):
    
    tool = models.CharField(max_length=10, choices=tools.get_tool_choices())
    user = models.ForeignKey(User)
    platter = models.ForeignKey(Platter)
    reservation_date = models.DateTimeField(auto_now_add=True)
    growth_length_in_hours = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=500, blank=True)
    bake_length_in_minutes = models.IntegerField()
    max_integer_value = 9223372036854775807
    priority_field = models.BigIntegerField(default=max_integer_value)
    is_active = models.BooleanField(default=True)
    def __str__(self):              # __unicode__ on Python 2
        return '{0}, {1}, {2}'.format(str(self.tool), str(self.user), str(self.growth_length_in_hours))
