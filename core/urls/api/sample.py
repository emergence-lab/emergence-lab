# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.api


urlpatterns = [
    url(r'^$', core.api.SampleListAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/$', core.api.SampleRetrieveAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/node/n(?P<node_uuid>[0-9a-f\-]{7,})/$',
        core.api.SampleNodeRetrieveAPIView.as_view()),
    url(r'^p?(?P<uuid>[0-9a-f\-]{7,})/node/tree/by_process/$',
        core.api.SampleByProcessAPIView.as_view()),
    url(r'^n?(?P<uuid>[0-9a-f\-]{7,})/node/tree/relative/$',
        core.api.SampleTreeNodeRelativeAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/node/tree/$',
        core.api.SampleTreeNodeAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/node/leaf/$',
        core.api.SampleLeafNodeAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/node/piece/(?P<piece>[a-z]+)/$',
        core.api.SamplePieceNodeAPIView.as_view()),
    url(r'^s(?P<uuid>[0-9]+)/node/piece/(?P<piece>[a-z]+)/leaf/$',
        core.api.SampleLeafNodeAPIView.as_view()),
    url(r'^substrate/$', core.api.SubstrateListAPIView.as_view()),
]
