# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from d180 import api


urlpatterns = [
    url(r'^readings/$', api.D180ReadingsListAPI.as_view()),
    url(r'^readings/(?P<pk>\d+)/$', api.D180ReadingsDetailAPI.as_view()),
    url(r'^readings/create/$', api.D180ReadingsCreateAPI.as_view()),
]
