# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.views

urlpatterns = [
    url(r'^$', core.views.ProcessListRedirectView.as_view(),
        name='process_list_redirect'),
    url(r'^list/(?P<slug>[\w-]+)/(?P<username>[\w-]+)/$',
        core.views.ProcessListView.as_view(), name='process_list'),
    url(r'^create/$', core.views.ProcessWizardView.as_view(),
        name='process_create'),
    url(r'^autocreate/(?P<uuid>s[0-9]+)(?P<piece>[a-z]+)?/$',
        core.views.RunProcessView.as_view(), name='process_autocreate'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/$', core.views.ProcessDetailView.as_view(),
        name='process_detail'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/edit/$',
        core.views.ProcessUpdateView.as_view(), name='process_edit'),
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/upload/$',
        core.views.UploadFileView.as_view(), name='file_upload'),
    url(r'^templates/(?P<slug>[\w-]+)/$',
        core.views.ProcessTemplateListView.as_view(), name='process_templates'),
    url(r'^templates/add/(?P<uuid>p[0-9a-f\-]{7,})/$',
        core.views.AddProcessTemplateView.as_view(), name='add_process_template'),
    url(r'^create/(?P<id>[0-9]+)$', core.views.TemplateProcessWizardView.as_view(),
        name='process_create_from_template'),
    url(r'^create/(?P<uuid>p[0-9a-f\-]{7,})$',
        core.views.TemplateProcessWizardView.as_view(),
        name='process_create_from_template'),
    url(r'^templates/detail/(?P<pk>[0-9]+)/$',
        core.views.ProcessTemplateDetailView.as_view(), name='process_template_detail'),
    url(r'^templates/edit/(?P<pk>[0-9]+)/$',
        core.views.ProcessTemplateEditView.as_view(), name='process_template_edit'),
    url(r'^templates/remove/(?P<pk>[0-9]+)/$',
        core.views.RemoveProcessTemplateView.as_view(), name='remove_process_template'),
]
