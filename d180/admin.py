# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

import d180.models


class GrowthAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created', 'user',)
    list_filter = ('user', 'investigations',)


admin.site.register(d180.models.D180Growth, GrowthAdmin)
admin.site.register(d180.models.Platter)
