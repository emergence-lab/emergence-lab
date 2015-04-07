# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import d180.views


urlpatterns = [
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/$',
        d180.views.ReadingsDetailView.as_view(), name='d180_readings_detail'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/edit/$',
        d180.views.UpdateReadingsView.as_view(), name='d180_readings_edit'),
]
