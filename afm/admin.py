# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

import afm.models


admin.site.register(afm.models.AFMScan)
