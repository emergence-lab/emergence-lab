# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url


urlpatterns = [
    url(r'^project/', include('project_management.urls.api.project')),
    url(r'^investigation/', include('project_management.urls.api.investigation')),
    url(r'^milestone/', include('project_management.urls.api.milestone')),
]
