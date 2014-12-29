# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

import core.api


urlpatterns = [
    url(r'^$', core.api.UserListAPIView.as_view()),
]
