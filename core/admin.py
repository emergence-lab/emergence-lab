from django.contrib import admin

import core.models


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project', 'active', 'start_date')
    list_filter = ('project', 'active')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'start_date')
    list_filter = ('active',)


admin.site.register(core.models.operator)
admin.site.register(core.models.platter)
admin.site.register(core.models.project, ProjectAdmin)
admin.site.register(core.models.investigation, InvestigationAdmin)
