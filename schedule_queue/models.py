# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models

from core.models import ActiveStateMixin, TimestampMixin, ProcessType
from d180.models import Platter


class Reservation(ActiveStateMixin, TimestampMixin, models.Model):
    MAX_PRIORITY = 9223372036854775807

    tool = models.ForeignKey(ProcessType, related_name='reservations',
                             related_query_name='reservation',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    platter = models.ForeignKey(Platter, on_delete=models.SET_NULL, null=True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    growth_length = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=500, blank=True)
    bake_length = models.IntegerField()
    priority = models.BigIntegerField(default=MAX_PRIORITY)

    @staticmethod
    def get_latest(user, process_type):
        return (Reservation.active_objects.filter(user=user, tool=process_type)
                                          .order_by('priority')
                                          .first())

    def increase_priority(self, save=True):
        next_item = (Reservation.active_objects.filter(priority__lt=self.priority)
                                               .order_by('-priority')
                                               .first())
        if not next_item:
            return None

        next_item.priority, self.priority = self.priority, next_item.priority
        if save:
            next_item.save()
            self.save()
        return next_item

    def decrease_priority(self, save=True):
        next_item = (Reservation.active_objects.filter(priority__gt=self.priority)
                                               .order_by('priority')
                                               .first())
        if not next_item:
            return None

        next_item.priority, self.priority = self.priority, next_item.priority
        if save:
            next_item.save()
            self.save()
        return next_item
