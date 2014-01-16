from django.conf.urls import patterns, include, url
from django.contrib import admin

import growths.views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wbg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', growths.views.growth_list.as_view(), name='afm_filter'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', growths.views.growth_detail.as_view(), name='growth_detail'),
    url(r'^afm-(?P<pk>\d+)/$', growths.views.afm_detail.as_view(), name='afm_detail'),
    url(r'^admin/', include(admin.site.urls)),
)
