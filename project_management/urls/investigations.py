from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^$', views.InvestigationListView.as_view(),
        name='pm_investigation_list'),
    url(r'^detail/(?P<slug>[\w-]+)$', views.InvestigationDetailView.as_view(),
        name='pm_investigation_detail'),
    url(r'^create$', views.InvestigationCreateView.as_view(),
        name='pm_investigation_create'),
]
