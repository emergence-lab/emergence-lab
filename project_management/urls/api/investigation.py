# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.api


urlpatterns = [
    url(r'^$', project_management.api.InvestigationListAPIView.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)$',
        project_management.api.InvestigationRetrieveAPIView.as_view()),
    url(r'^edit/(?P<slug>[\w-]+)$', project_management.api.InvestigationUpdateAPIView.as_view()),
    url(r'^processes/(?P<slug>[\w-]+)$',
        project_management.api.InvestigationProcessListAPIView.as_view()),
]
