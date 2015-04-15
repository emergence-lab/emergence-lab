# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import d180.views


urlpatterns = [
    url(r'^create/start/$',
        d180.views.WizardStartView.as_view(), name='create_growth_d180_start'),
    url(r'^create/readings/$',
        d180.views.WizardReadingsView.as_view(),
        name='create_growth_d180_readings'),
    url(r'^create/postrun/$',
        d180.views.WizardPostrunView.as_view(),
        name='create_growth_d180_postrun'),
]
