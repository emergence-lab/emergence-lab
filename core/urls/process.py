# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.views

urlpatterns = [
    url(r'^$', core.views.ProcessListView.as_view(), name='process_list'),
    url(r'^filter/(?P<slug>[\w-]+)$', core.views.ProcessListViewFilter.as_view(), name='process_list_filter'),
    url(r'^create/$', core.views.ProcessCreateView.as_view(),
        name='process_create'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/$', core.views.ProcessDetailView.as_view(),
        name='process_detail'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/edit/$',
        core.views.ProcessUpdateView.as_view(), name='process_edit'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/upload/$',
        core.views.UploadFileView.as_view(), name='file_upload'),
]
