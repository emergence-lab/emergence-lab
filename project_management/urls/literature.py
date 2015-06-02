from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import project_management.views as views


urlpatterns = [
    url(r'^list$',
        views.LiteratureListView.as_view(),
        name="literature_list"),
    url(r'^search$',
        views.MendeleyLibrarySearchView.as_view(),
        name="mendeley_search"),
    url(r'^$',
        views.LiteratureLandingView.as_view(),
        name="literature_landing"),
    url(r'^add/(?P<milestone>[0-9]+)/(?P<external_id>[0-9a-f\w-]{36,})$',
        views.AddMendeleyObjectView.as_view(),
        name="add_mendeley_object"),
    url(r'^add/(?P<investigation>[0-9]+)/(?P<external_id>[0-9a-f\w-]{36,})$',
        views.AddMendeleyObjectView.as_view(),
        name="add_mendeley_object"),
    ]
