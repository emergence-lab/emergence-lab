# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.views

urlpatterns = [
    url(r'^$', core.views.SampleListView.as_view(), name='sample_list'),
    url(r'^create/$', core.views.SampleCreateView.as_view(),
        name='sample_create'),
    url(r'^search/$', core.views.SampleSearchView.as_view(),
        name='sample_search'),
    url(r'^(?P<uuid>s[0-9]+)/$', core.views.SampleDetailView.as_view(),
        name='sample_detail'),
    url(r'^(?P<uuid>s[0-9]+)/edit/$', core.views.SampleUpdateView.as_view(),
        name='sample_edit'),
    url(r'^(?P<uuid>s[0-9]+)/run/$', core.views.RunProcessView.as_view(),
        name='run_process'),
    url(r'^split/(?P<uuid>s[0-9]+)/(?P<piece>[a-z]+)/$',
        core.views.SampleSplitView.as_view(), name='split_sample'),
]
