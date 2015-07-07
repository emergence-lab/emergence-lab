# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from schedule_queue import views


urlpatterns = [
    url(r'^$', views.ReservationLanding.as_view(), name='reservation_landing'),
    url(r'^create/$',
        views.ReservationCreate.as_view(), name='reservation_create'),
    url(r'^edit/(?P<pk>\d+)/$',
        views.ReservationEdit.as_view(), name='reservation_edit'),
    url(r'^cancel/(?P<pk>\d+)/$',
        views.CancelReservation.as_view(), name='cancel_reservation'),
    url(r'^close/(?P<pk>\d+)/$',
        views.CloseReservation.as_view(), name='close_reservation'),
    url(r'^increase/(?P<pk>\d+)/$',
        views.IncreasePriority.as_view(), name='increase_priority'),
    url(r'^decrease/(?P<pk>\d+)/$',
        views.DecreasePriority.as_view(), name='decrease_priority'),
    url(r'^list/(?P<process>[a-z0-9\-]+)/$',
        views.ReservationList.as_view(), name='reservation_list'),
]
