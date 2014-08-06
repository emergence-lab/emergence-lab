from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
import django.contrib
from rest_framework.urlpatterns import format_suffix_patterns

import core.views
import growths.views
import afm.views
import afm.api
import hall.views


admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.auth.views',
    # urls, add login_required() around the as_view() call for security
    # misc urls
    url(r'^media/(?P<filename>.*)$', login_required(core.views.protected_media)),
    url(r'^$', core.views.homepage.as_view(), name='home'),
    url(r'^quicksearch/', login_required(core.views.QuickSearchRedirect.as_view()), name='quicksearch'),
    url(r'^exception/', login_required(core.views.ExceptionHandlerView.as_view()), name='exception'),
    url(r'^profile/', login_required(core.views.Dashboard.as_view()), name='profile_dashboard'),
    url(r'^accounts/login/', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # core urls
    url(r'^operators/$', login_required(core.views.operator_list.as_view()), name='operator_list'),
    url(r'^operators/create/$', login_required(core.views.operator_create.as_view()), name='operator_create'),
    url(r'^platters/$', login_required(core.views.platter_list.as_view()), name='platter_list'),
    url(r'^projects/$', login_required(core.views.project_list.as_view()), name='project_list'),
    url(r'^projects/(?P<slug>[\w-]+)/$', login_required(core.views.ProjectDetailView.as_view()), name='project_detail'),
    url(r'^investigations/$', login_required(core.views.investigation_list.as_view()), name='investigation_list'),
    # growths urls
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', login_required(growths.views.GrowthDetailView.as_view()), name='growth_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/recipe/$', login_required(growths.views.recipe_detail.as_view()), name='recipe_detail'),
    url(r'^sample/(?P<pk>\d+)/$', login_required(growths.views.SampleDetailView.as_view()), name='sample_detail'),
    url(r'^(?P<growth>[gt][1-9][0-9]{3,})/(?P<pocket>\d+\-?\d*)/$', login_required(growths.views.SampleFamilyDetailView.as_view()), name='sample_family_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/$', login_required(growths.views.readings_detail.as_view()), name='readings_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/update/$', login_required(growths.views.update_readings.as_view()), name='update_readings'),
    # afm urls
    url(r'^afm/$', login_required(afm.views.AFMList.as_view()), name='afm_list'),
    url(r'^afm/(?P<pk>\d+)/$', login_required(afm.views.AFMDetail.as_view()), name='afm_detail'),
    url(r'^afm/create/$', login_required(afm.views.AFMCreate.as_view()), name='afm_create'),
    url(r'^afm/(?P<pk>\d+)/update/$', login_required(afm.views.AFMUpdate.as_view()), name='afm_update'),
    url(r'^afm/(?P<pk>\d+)/delete/$', login_required(afm.views.AFMDelete.as_view()), name='afm_delete'),
    # afm rest framework
    url(r'^api/v0/afm/$', afm.api.AFMListAPI.as_view()),
    url(r'^api/v0/afm/(?P<pk>\d+)/$', afm.api.AFMDetailAPI.as_view()),
    # hall urls
    url(r'^hall/$', login_required(hall.views.hall_list.as_view()), name='hall_list'),
    url(r'^hall/(?P<pk>\d+)/$', login_required(hall.views.hall_detail.as_view()), name='hall_detail'),
    # creategrowth urls
    url(r'^creategrowth/$', login_required(growths.views.create_growth), name='create_growth'),
    url(r'^splitsample/$', login_required(growths.views.split_sample), name='split_sample'),

    url(r'^creategrowth/start/$', login_required(growths.views.create_growth_start), name='create_growth_start'),
    url(r'^creategrowth/prerun/$', login_required(growths.views.create_growth_prerun), name='create_growth_prerun'),
    url(r'^creategrowth/readings/$', login_required(growths.views.create_growth_readings.as_view()), name='create_growth_readings'),
    url(r'^creategrowth/postrun/$', login_required(growths.views.create_growth_postrun), name='create_growth_postrun'),
    # advanced views
    url(r'^afm-compare/$', login_required(growths.views.afm_compare.as_view()), name='afm_compare'),
    url(r'^afm-filter/$', login_required(growths.views.growth_list.as_view()), name='afm_filter'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
