# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

import core.models
from core.forms.user import CreateUserForm


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project', 'is_active', 'created')
    list_filter = ('project', 'is_active')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created')
    list_filter = ('is_active',)


class ProjectTrackingInline(admin.TabularInline):
    model = core.models.ProjectTracking
    extra = 1


class UserAdmin(admin.ModelAdmin):
    form = CreateUserForm


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('uuid_full', 'legacy_identifier', 'type', 'user',
                    'run_date', 'created', 'modified',)
    list_filter = ('type', 'user', 'run_date', 'created', 'modified',)
    save_as = True


class ProcessTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'category', 'is_destructive',
                    'scheduling_type', 'creation_type',)
    list_filter = ('category', 'is_destructive', 'scheduling_type', 'creation_type',)


class ProcessCategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)


class ProcessNodeAdmin(admin.ModelAdmin):
    list_display = ('uuid_full', 'sample', 'tree_id', 'level', 'piece', 'number',
                    'process_uuid', 'process_type', 'created', 'modified',)
    list_filter = ('tree_id', 'piece', 'created', 'modified',)

    def process_uuid(self, obj):
        if obj.process:
            return obj.process.uuid_full
        return None

    def process_type(self, obj):
        if obj.process:
            return obj.process.type
        return None


class SampleAdmin(admin.ModelAdmin):
    list_display = ('uuid_full', 'substrate', 'process_tree', 'num_processes',
                    'num_pieces', 'created', 'modified',)

    def num_processes(self, obj):
        return len(obj.processes)

    def num_pieces(self, obj):
        return len(obj.pieces)


class SubstrateAdmin(admin.ModelAdmin):
    list_display = ('serial', 'source', 'created', 'modified',)


admin.site.register(core.models.Project, ProjectAdmin)
admin.site.register(core.models.Investigation, InvestigationAdmin)
admin.site.register(core.models.ProjectTracking)
admin.site.register(core.models.Milestone)
admin.site.register(core.models.User, UserAdmin)
admin.site.register(core.models.Process, ProcessAdmin)
admin.site.register(core.models.ProcessType, ProcessTypeAdmin)
admin.site.register(core.models.ProcessCategory, ProcessCategoryAdmin)
admin.site.register(core.models.ProcessNode, ProcessNodeAdmin)
admin.site.register(core.models.Sample, SampleAdmin)
admin.site.register(core.models.Substrate, SubstrateAdmin)
