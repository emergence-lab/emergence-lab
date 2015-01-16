# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from messaging import api


urlpatterns = [
    url(r'^notifications/create/$', api.NotificationCreateAPI.as_view()),
]
