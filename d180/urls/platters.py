# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import d180.views


urlpatterns = [
    url(r'^$', d180.views.PlatterListView.as_view(), name='platter_list'),
    url(r'^create/$',
        d180.views.PlatterCreateView.as_view(), name='platter_create'),
    url(r'^(?P<id>\d+)/activate/$',
        d180.views.ActivatePlatterReloadView.as_view(),
        name='platter_activate'),
    url(r'^(?P<id>\d+)/deactivate/$',
        d180.views.DeactivatePlatterReloadView.as_view(),
        name='platter_deactivate'),
]
