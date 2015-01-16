# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import afm.views


urlpatterns = [
    url(r'^$', afm.views.AFMList.as_view(), name='afm_list'),
    url(r'^create/$', afm.views.AFMCreate.as_view(), name='afm_create'),
    url(r'^(?P<pk>\d+)/$', afm.views.AFMDetail.as_view(), name='afm_detail'),
    url(r'^(?P<pk>\d+)/update/$',
        afm.views.AFMUpdate.as_view(), name='afm_update'),
    url(r'^(?P<pk>\d+)/delete/$',
        afm.views.AFMDelete.as_view(), name='afm_delete'),
]
