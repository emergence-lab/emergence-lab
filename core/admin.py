from django.contrib import admin

import core.models


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project', 'is_active', 'created')
    list_filter = ('project', 'is_active')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created')
    list_filter = ('is_active',)


class ProjectTrackingInline(admin.TabularInline):
    model = core.models.project_tracking
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    inlines = (ProjectTrackingInline, )
    fields = ('name', 'is_active', 'user')


admin.site.register(core.models.operator, OperatorAdmin)
admin.site.register(core.models.project, ProjectAdmin)
admin.site.register(core.models.investigation, InvestigationAdmin)
admin.site.register(core.models.project_tracking)
