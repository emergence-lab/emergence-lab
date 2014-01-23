from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

import growths.views


admin.autodiscover()

urlpatterns = patterns(
    '',
    # urls, add login_required() around the as_view() call for security
    url(r'^$', growths.views.growth_list.as_view(), name='afm_filter'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', growths.views.growth_detail.as_view(), name='growth_detail'),
    url(r'^afm-(?P<pk>\d+)/$', growths.views.afm_detail.as_view(), name='afm_detail'),
    url(r'^afm-compare/$', growths.views.afm_compare.as_view(), name='afm_compare'),
    url(r'^admin/', include(admin.site.urls)),
)
