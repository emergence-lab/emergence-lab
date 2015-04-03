# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import afm.views


urlpatterns = [
    url(r'^$', afm.views.AFMList.as_view(), name='afm_list'),
    url(r'^create/$', afm.views.AFMCreate.as_view(), name='afm_create'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/$',
        afm.views.AFMDetail.as_view(), name='afm_detail'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/update/$',
        afm.views.AFMUpdate.as_view(), name='afm_update'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/delete/$',
        afm.views.AFMDelete.as_view(), name='afm_delete'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/upload/$',
        afm.views.AFMFileUpload.as_view(), name='afm_upload'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/remove/(?P<id>[0-9]+)/$',
        afm.views.AFMRemoveFileActionReloadView.as_view(), name='afm_file_remove'),
]
