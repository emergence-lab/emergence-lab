from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
import django.contrib

import core.views
import growths.views


admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.auth.views',
    # urls, add login_required() around the as_view() call for security
    url(r'^$', core.views.homepage.as_view(), name='home'),
    url(r'^afm-filter/$', login_required(growths.views.growth_list.as_view()), name='afm_filter'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', login_required(growths.views.growth_detail.as_view()), name='growth_detail'),
    url(r'^afm-(?P<pk>\d+)/$', growths.views.afm_detail.as_view(), name='afm_detail'),
    url(r'^afm-compare/$', login_required(growths.views.afm_compare.as_view()), name='afm_compare'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'core/logout.html'}, name='logout')
)
