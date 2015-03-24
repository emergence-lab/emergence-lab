# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

import rest_framework.authtoken.views


urlpatterns = [
    url(r'^token/', rest_framework.authtoken.views.obtain_auth_token),
    url(r'^users/', include('core.urls.api.user')),
    url(r'^process/', include('core.urls.api.process')),
    url(r'^sample/', include('core.urls.api.sample')),
    url(r'^utility/', include('core.urls.api.utility')),
    url(r'^afm/', include('afm.urls.api')),
    url(r'^sem/', include('sem.urls.api')),
    url(r'^messaging/', include('messaging.urls.api')),
    url(r'^d180/', include('d180.urls.api')),
    url(r'^hall/', include('hall.urls.api')),
]
