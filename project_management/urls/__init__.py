# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^list/$',
        views.MilestoneListView.as_view(),
        name='milestone_list'),
    url(r'^create/$',
        views.MilestoneCreateView.as_view(),
        name='milestone_create'),
    url(r'^detail/(?P<pk>[0-9]+)$',
        views.MilestoneDetailView.as_view(),
        name="milestone_detail"),
    ]
