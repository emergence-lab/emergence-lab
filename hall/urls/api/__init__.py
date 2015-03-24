# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import hall.api


urlpatterns = [
    url(r'^$', hall.api.HallListCreateAPIView.as_view()),
    url(r'^(?P<pk>\d+)/$', hall.api.HallRetrieveUpdateAPIView.as_view()),
]
