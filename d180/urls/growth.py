# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import d180.views


urlpatterns = [
    url(r'^create/start/$',
        d180.views.WizardStartView.as_view(), name='create_growth_d180_start'),
    url(r'^create/start/(?P<id>[0-9]+)$',
        d180.views.TemplateWizardStartView.as_view(),
        name='create_growth_d180_start_template'),
    url(r'^create/start/(?P<uuid>p[0-9a-f\-]{7,})$',
        d180.views.TemplateWizardStartView.as_view(),
        name='create_growth_d180_start_template'),
    url(r'^create/readings/$',
        d180.views.WizardReadingsView.as_view(),
        name='create_growth_d180_readings'),
    url(r'^create/postrun/$',
        d180.views.WizardPostrunView.as_view(),
        name='create_growth_d180_postrun'),
    url(r'^create/cancel/$',
        d180.views.WizardCancelView.as_view(),
        name='create_growth_d180_cancel'),
]
