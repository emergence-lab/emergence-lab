# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

import project_management.views as views


urlpatterns = [
    url(r'^milestones/', include('project_management.urls.milestones')),
    url(r'^literature/', include('project_management.urls.literature')),
    url(r'^investigations/', include('project_management.urls.investigations')),
    url(r'^projects/', include('project_management.urls.projects')),
    url(r'^tasks/', include('project_management.urls.tasks')),
    url(r'^$', views.LandingPageView.as_view(), name="dashboard"),
    url(r'^newsfeed$', views.NewsfeedView.as_view(), name="pm_newsfeed"),
    ]
