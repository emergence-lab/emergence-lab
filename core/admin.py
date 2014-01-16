from django.contrib import admin
from .models import operator, platter, project, growth, afm, investigation


class growth_admin(admin.ModelAdmin):
    fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
              'run_comments', 'carrier_number']


admin.site.register(operator)
admin.site.register(platter)
admin.site.register(project)
admin.site.register(growth, growth_admin)
admin.site.register(afm)
admin.site.register(investigation)
