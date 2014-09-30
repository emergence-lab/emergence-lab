from django.contrib import admin

import core.models


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project', 'active', 'created')
    list_filter = ('project', 'active')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'created')
    list_filter = ('active',)


class ProjectTrackingInline(admin.TabularInline):
    model = core.models.project_tracking
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    inlines = (ProjectTrackingInline, )
    fields = ('name', 'active', 'user')


admin.site.register(core.models.operator, OperatorAdmin)
admin.site.register(core.models.platter)
admin.site.register(core.models.project, ProjectAdmin)
admin.site.register(core.models.investigation, InvestigationAdmin)
admin.site.register(core.models.project_tracking)
