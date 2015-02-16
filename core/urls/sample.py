# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.views

urlpatterns = [
    url(r'^$', core.views.SampleListView.as_view(), name='sample_list'),
    url(r'^(?P<uuid>s[0-9]+)/$', core.views.SampleDetailView.as_view(),
        name='sample_detail'),
]
