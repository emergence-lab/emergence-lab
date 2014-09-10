from django.contrib import admin

import growths.models


class SampleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent', 'size', 'location', 'substrate_serial')
    ordering = ('-growth__growth_number', 'pocket', 'piece')


class GrowthAdmin(admin.ModelAdmin):
    list_display = ('growth_number', 'date', 'operator', 'project',
                    'investigation', 'reactor')
    ordering = ('-growth_number',)
    list_filter = ('operator', 'project', 'investigation', 'reactor')


admin.site.register(growths.models.growth, GrowthAdmin)
admin.site.register(growths.models.sample, SampleAdmin)
