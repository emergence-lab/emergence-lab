# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from d180 import api


urlpatterns = [
    url(r'^readings/$', api.D180ReadingsListAPI.as_view()),
]
