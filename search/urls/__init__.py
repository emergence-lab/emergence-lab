# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import search.views


urlpatterns = [
    url(r'^$', search.views.ElasticSearchView.as_view(), name='es_search'),
    # url(r'^autocreate/(?P<uuid>s[0-9]+)(?P<piece>[a-z]+)?/$',
    #     sem.views.AutocreateSEMView.as_view(), name='sem_autocreate'),
]
