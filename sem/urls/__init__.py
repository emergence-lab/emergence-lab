# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import sem.views


urlpatterns = [
    url(r'^$', sem.views.SEMList.as_view(), name='sem_list'),
    url(r'^create/$', sem.views.SEMCreate.as_view(), name='sem_create'),
    url(r'^autocreate/(?P<uuid>s[0-9]+)/$', sem.views.SEMAutoCreate.as_view(), name='sem_autocreate'),
    url(r'^(?P<pk>\d+)/$', sem.views.SEMDetail.as_view(), name='sem_detail'),
    url(r'^(?P<pk>\d+)/update/$',
        sem.views.SEMUpdate.as_view(), name='sem_update'),
    url(r'^(?P<pk>\d+)/delete/$',
        sem.views.SEMDelete.as_view(), name='sem_delete'),
    url(r'^(?P<pk>\d+)/add_files/$',
        sem.views.SEMAddFiles.as_view(), name='sem_files'),
]
