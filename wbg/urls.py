from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
import django.contrib

import core.views
import growths.views
import afm.views
import hall.views


admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.auth.views',
    # urls, add login_required() around the as_view() call for security
    # misc urls
    url(r'^media/(?P<filename>.*)$', login_required(core.views.protected_media)),
    url(r'^$', core.views.homepage.as_view(), name='home'),
    url(r'^accounts/login/', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # core urls
    url(r'^operators/$', login_required(core.views.operator_list.as_view()), name='operator_list'),
    url(r'^operators/create/$', login_required(core.views.operator_create.as_view()), name='operator_create'),
    url(r'^platters/$', login_required(core.views.platter_list.as_view()), name='platter_list'),
    url(r'^projects/$', login_required(core.views.project_list.as_view()), name='project_list'),
    url(r'^investigations/$', login_required(core.views.investigation_list.as_view()), name='investigation_list'),
    # growths urls
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', login_required(growths.views.growth_detail.as_view()), name='growth_detail'),
    # afm urls
    url(r'^afm/(?P<pk>\d+)/$', login_required(afm.views.afm_detail.as_view()), name='afm_detail'),
    url(r'^afm/create/$', login_required(afm.views.afm_create.as_view()), name='afm_create'),
    # hall urls
    url(r'^hall/$', login_required(hall.views.hall_list.as_view()), name='hall_list'),
    url(r'^hall/(?P<pk>\d+)/$', login_required(hall.views.hall_detail.as_view()), name='hall_detail'),
    # creategrowth urls
    url(r'^creategrowth/$', login_required(growths.views.create_growth), name='create_growth'),
    url(r'^splitsample/$', login_required(growths.views.split_sample), name='split_sample'),
    # advanced views
    url(r'^afm-compare/$', login_required(growths.views.afm_compare.as_view()), name='afm_compare'),
    url(r'^afm-filter/$', login_required(growths.views.growth_list.as_view()), name='afm_filter'),
)
