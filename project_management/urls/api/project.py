# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.api


urlpatterns = [
    url(r'^$', project_management.api.ProjectListFollowedAPIView.as_view()),
    url(r'^all$', project_management.api.ProjectListAllAPIView.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)$', project_management.api.ProjectRetrieveAPIView.as_view()),
    url(r'^edit/(?P<slug>[\w-]+)$', project_management.api.ProjectUpdateAPIView.as_view()),
    url(r'^untrack/(?P<slug>[\w-]+)$', project_management.api.ProjectUntrackAPIView.as_view()),
    url(r'^track/(?P<slug>[\w-]+)$', project_management.api.ProjectTrackAPIView.as_view()),
]
