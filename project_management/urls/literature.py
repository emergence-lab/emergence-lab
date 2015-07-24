from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^search$',
        views.MendeleyLibrarySearchView.as_view(),
        name="mendeley_search"),
    url(r'^$',
        views.LiteratureLandingView.as_view(),
        name="literature_landing"),
    url(r'^add/external/milestone/(?P<milestone>[0-9]+)/(?P<external_id>[0-9a-f\w-]{36,})$',
        views.AddMendeleyObjectView.as_view(),
        name="add_mendeley_object_milestone"),
    url(r'^add/external/investigation/(?P<investigation>[0-9]+)/(?P<external_id>[0-9a-f\w-]{36,})$',
        views.AddMendeleyObjectView.as_view(),
        name="add_mendeley_object_investigation"),
    url(r'^add/existing/milestone/(?P<milestone>[0-9]+)/(?P<pk>[0-9]+)$',
        views.AddMendeleyObjectView.as_view(),
        name="add_literature_object_milestone"),
    url(r'^add/existing/investigation/(?P<investigation>[0-9]+)/(?P<pk>[0-9]+)$',
        views.AddMendeleyObjectView.as_view(),
        name="add_literature_object_investigation"),
    url(r'^create$',
        views.CreateLiteratureObjectView.as_view(),
        name="literature_create"),
    url(r'^detail/redirect/(?P<pk>[0-9]+)$',
        views.LiteratureDetailRedirector.as_view(),
        name="literature_detail_redirector"),
    url(r'^detail/internal/(?P<pk>[0-9]+)$',
        views.LiteratureDetailView.as_view(),
        name="literature_detail"),
    url(r'^detail/external/(?P<external_id>[0-9a-f\w-]{36,})$',
        views.MendeleyDetailView.as_view(),
        name="mendeley_detail"),
    ]
