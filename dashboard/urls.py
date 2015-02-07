# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^add_action/$',
        views.AddActionItemView.as_view(), name='add_action_item'),
    url(r'^delete_action/(?P<action_item>\d+)$',
        views.RemoveActionItemView.as_view(), name='remove_action_item'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.ProjectDetailDashboardView.as_view(),
        name='project_detail_dashboard'),
    url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.InvestigationDetailDashboardView.as_view(),
        name='investigation_detail_dashboard'),
]
