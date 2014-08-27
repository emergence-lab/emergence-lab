from django.contrib import admin
import core.models


class ProjectTrackingInline(admin.TabularInline):
    model = core.models.project_tracking
    extra = 1

class OperatorAdmin(admin.ModelAdmin):
    inlines = (ProjectTrackingInline, )
    fields = ('name', 'active', 'user')


admin.site.register(core.models.operator, OperatorAdmin)
admin.site.register(core.models.platter)
admin.site.register(core.models.project)
admin.site.register(core.models.investigation)
admin.site.register(core.models.project_tracking)
