from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(),
        name='pm_project_list'),
    url(r'^edit/(?P<slug>[\w-]+)$', views.ProjectUpdateView.as_view(),
        name='pm_project_edit'),
    url(r'^detail/(?P<slug>[\w-]+)$', views.ProjectDetailView.as_view(),
        name='pm_project_detail'),
    url(r'^group_add/(?P<slug>[\w-]+)/(?P<username>[\w-]+)/(?P<attribute>[\w]+)$',
        views.AddUserToProjectGroupView.as_view(),
        name='pm_project_group_add'),
    url(r'^group_remove/(?P<slug>[\w-]+)/(?P<username>[\w-]+)/$',
        views.RemoveUserFromProjectGroup.as_view(),
        name='pm_project_group_remove'),
    url(r'^admin$', views.ProjectGroupAdminView.as_view(),
        name='pm_project_admin'),
]
