# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

import core.models


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project', 'is_active', 'created')
    list_filter = ('project', 'is_active')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created')
    list_filter = ('is_active',)


class ProjectTrackingInline(admin.TabularInline):
    model = core.models.ProjectTracking
    extra = 1


admin.site.register(core.models.Project, ProjectAdmin)
admin.site.register(core.models.Investigation, InvestigationAdmin)
admin.site.register(core.models.ProjectTracking)
admin.site.register(core.models.Milestone)
