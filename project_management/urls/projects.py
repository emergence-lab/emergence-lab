from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(),
        name='pm_project_list'),
    url(r'^edit/(?P<slug>[\w-]+)$', views.ProjectUpdateView.as_view(),
        name='pm_project_edit')
]
