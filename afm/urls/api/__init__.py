# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import afm.api


urlpatterns = [
    url(r'^$', afm.api.AFMListCreateAPIView.as_view()),
    url(r'^(?P<pk>\d+)/$', afm.api.AFMRetrieveUpdateAPIView.as_view()),
]
