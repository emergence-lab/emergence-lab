from django.contrib import admin

import growths.models


class SampleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent_sample', 'size', 'location', 'substrate_serial')
    ordering = ('-growth__growth_number', 'pocket', 'piece')

    def parent_sample(self, instance):
        if instance.id == instance.parent_id:
            return None
        else:
            return instance.parent


class GrowthAdmin(admin.ModelAdmin):
    list_display = ('growth_number', 'date', 'operator', 'project',
                    'investigation', 'reactor')
    ordering = ('-growth_number',)
    list_filter = ('operator', 'project', 'investigation', 'reactor')


admin.site.register(growths.models.growth, GrowthAdmin)
admin.site.register(growths.models.sample, SampleAdmin)
admin.site.register(growths.models.Platter)
