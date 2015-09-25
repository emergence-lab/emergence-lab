# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.views

urlpatterns = [
    # url(r'^$',
    #     core.views.ProjectListView.as_view(), name='project_list'),
    url(r'^create/$',
        core.views.ProjectCreateView.as_view(), name='project_create'),
    url(r'^track/$',
        core.views.TrackProjectView.as_view(), name='track_project'),
    # url(r'^(?P<slug>[\w-]+)/$',
    #     core.views.ProjectDetailView.as_view(), name='project_detail_all'),
    # url(r'^(?P<slug>[\w-]+)/edit/$',
    #     core.views.ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<slug>[\w-]+)/track/$',
        core.views.TrackProjectRedirectView.as_view(), name='project_track'),
    url(r'^(?P<slug>[\w-]+)/untrack/$',
        core.views.UntrackProjectRedirectView.as_view(),
        name='project_untrack'),
    url(r'^(?P<slug>[\w-]+)/activate/$',
        core.views.ActivateProjectRedirectView.as_view(),
        name='project_activate'),
    url(r'^(?P<slug>[\w-]+)/deactivate/$',
        core.views.DeactivateProjectRedirectView.as_view(),
        name='project_deactivate'),
    # url(r'^(?P<slug>[\w-]+)/add-investigation/$',
    #     core.views.InvestigationCreateView.as_view(),
    #     name='investigation_create'),
    # url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$',
    #     core.views.InvestigationDetailView.as_view(),
    #     name='investigation_detail_all'),
    # url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/edit/$',
    #     core.views.InvestigationUpdateView.as_view(),
    #     name='investigation_update'),
    url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/activate/$',
        core.views.ActivateInvestigationRedirectView.as_view(),
        name='investigation_activate'),
    url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/deactivate/$',
        core.views.DeactivateInvestigationRedirectView.as_view(),
        name='investigation_deactivate'),
]
