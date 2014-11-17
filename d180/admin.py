from django.contrib import admin

import d180.models


class GrowthAdmin(admin.ModelAdmin):
    list_display = ('uid', 'created', 'user',)
    ordering = ('-uid',)
    list_filter = ('user', 'investigations',)


admin.site.register(d180.models.Growth, GrowthAdmin)
admin.site.register(d180.models.Platter)
