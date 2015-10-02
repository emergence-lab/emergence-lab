# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.api


urlpatterns = [
    url(r'^$', project_management.api.ProjectListAPIView.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)$', project_management.api.ProjectRetrieveAPIView.as_view()),
    url(r'^edit/(?P<slug>[\w-]+)$', project_management.api.ProjectUpdateAPIView.as_view()),
    # url(r'^detail/(?P<pk>[0-9a-f\-])$', project_management.api.ProjectRetrieveAPIView.as_view()),
]
