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
    ]
