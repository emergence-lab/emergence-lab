# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import afm.views


urlpatterns = [
    url(r'^(?P<uuid>p[0-9a-f\-]{7,})/upload/$',
        afm.views.AFMFileUpload.as_view(), name='afm_upload'),
    url(r'^autocreate/(?P<uuid>s[0-9]+)/$',
        afm.views.AutocreateAFMView.as_view(), name='afm_autocreate'),
]
