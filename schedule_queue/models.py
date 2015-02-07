# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import schedule_queue.config as tools

from core.models import ActiveStateMixin
from d180.models import Platter


@python_2_unicode_compatible
class Reservation(ActiveStateMixin, models.Model):

    @staticmethod
    def get_latest(user, tool_name):
        item = Reservation.objects.filter(is_active=True,
                                          tool=tool_name).order_by('priority_field').first()
        if item and item.user == user:
            return item
        else:
            return None

    tool = models.CharField(max_length=10, choices=tools.get_tool_choices())
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    platter = models.ForeignKey(Platter)
    reservation_date = models.DateTimeField(auto_now_add=True)
    growth_length_in_hours = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=500, blank=True)
    bake_length_in_minutes = models.IntegerField()
    max_integer_value = 9223372036854775807
    priority_field = models.BigIntegerField(default=max_integer_value)

    def __str__(self):
        return '{0}, {1}, {2}'.format(str(self.tool),
                                      str(self.user),
                                      str(self.growth_length_in_hours))
