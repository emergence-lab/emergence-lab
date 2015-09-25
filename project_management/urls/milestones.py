from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^list/$',
        views.MilestoneListView.as_view(),
        name='milestone_list'),
    url(r'^create/(?P<investigation>[\w-]+)$',
        views.MilestoneCreateView.as_view(),
        name='milestone_create'),
    url(r'^detail/(?P<slug>[\w-]+)$',
        views.MilestoneDetailView.as_view(),
        name="milestone_detail"),
    url(r'^edit/(?P<slug>[\w-]+)$',
        views.MilestoneUpdateView.as_view(),
        name="milestone_edit"),
    url(r'^open/(?P<slug>[\w-]+)$',
        views.MilestoneReOpenView.as_view(),
        name="milestone_open"),
    url(r'^close/(?P<slug>[\w-]+)$',
        views.MilestoneCloseView.as_view(),
        name="milestone_close"),
    url(r'^note/$',
        views.MilestoneNoteAction.as_view(),
        name='milestone_note_action'),
    ]
