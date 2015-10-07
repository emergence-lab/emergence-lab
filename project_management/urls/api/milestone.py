# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.api


urlpatterns = [
    url(r'^$', project_management.api.MilestoneListAPIView.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)$',
        project_management.api.MilestoneRetrieveAPIView.as_view()),
    url(r'^edit/(?P<slug>[\w-]+)$', project_management.api.MilestoneUpdateAPIView.as_view()),
    url(r'^processes/(?P<slug>[\w-]+)$',
        project_management.api.MilestoneProcessListAPIView.as_view()),
]
