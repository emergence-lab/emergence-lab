# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import hall.views


urlpatterns = [
    url(r'^$', hall.views.HallListView.as_view(), name='hall_list'),
    url(r'^(?P<pk>\d+)/$', hall.views.HallDetailView.as_view(), name='hall_detail'),
]
