from django.contrib import admin
import growths.models


admin.site.register(growths.models.growth)
admin.site.register(growths.models.sample)
