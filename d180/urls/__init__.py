# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include


urlpatterns = [
    url(r'^platters/', include('d180.urls.platters')),
    url(r'^growth/', include('d180.urls.growth')),
]
