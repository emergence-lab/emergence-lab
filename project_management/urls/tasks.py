from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^$', views.TaskListView.as_view(),
        name='pm_task_list'),
    url(r'^new$', views.TaskCreateView.as_view(),
        name='task_create'),
    # url(r'^edit/(?P<slug>[\w-]+)$', views.ProjectUpdateView.as_view(),
    #     name='pm_project_edit')
    url(r'^open/(?P<pk>[0-9]+)$', views.TaskReOpenView.as_view(),
        name='task_open'),
    url(r'^close/(?P<pk>[0-9]+)$', views.TaskCloseView.as_view(),
        name='task_close'),
]
