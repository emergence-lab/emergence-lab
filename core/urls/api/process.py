# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.api


urlpatterns = [
    url(r'^$', core.api.ProcessListAPIView.as_view()),
    url(r'^p?(?P<uuid>[0-9a-f\-]{7})/$',
        core.api.ProcessRetrieveAPIView.as_view()),
    url(r'^node/n?(?P<uuid>[0-9a-f\-]{7})/$',
        core.api.ProcessNodeRetrieveAPIView.as_view()),
]
