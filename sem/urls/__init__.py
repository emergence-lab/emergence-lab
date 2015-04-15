# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import sem.views


urlpatterns = [
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/upload/$',
        sem.views.SEMFileUpload.as_view(), name='sem_upload'),
    url(r'^autocreate/(?P<uuid>s[0-9]+)(?P<piece>[a-z]+)?/$',
        sem.views.AutocreateSEMView.as_view(), name='sem_autocreate'),
]
