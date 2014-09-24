from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.views.decorators.cache import never_cache
import django.contrib
from rest_framework.urlpatterns import format_suffix_patterns

import core.views
import growths.views
import afm.api


admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^ckeditor/', include('ckeditor.urls')),
    # urls, add login_required() around the as_view() call for security

    # misc urls
    url(r'^$', core.views.HomepageView.as_view(), name='home'),
    url(r'^media/(?P<filename>.*)$', core.views.protected_media),
    url(r'^quicksearch/', core.views.QuickSearchRedirectView.as_view(), name='quicksearch'),
    url(r'^exception/', core.views.ExceptionHandlerView.as_view(), name='exception'),
    url(r'^accounts/login/', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^wbg-admin/', include(admin.site.urls)),

    # core urls
    url(r'^operators/$', core.views.OperatorListView.as_view(), name='operator_list'),
    url(r'^operators/(?P<id>\d+)/activate$', never_cache(core.views.ActivateOperatorRedirectView.as_view()), name='operator_activate'),
    url(r'^operators/(?P<id>\d+)/deactivate$', never_cache(core.views.DeactivateOperatorRedirectView.as_view()), name='operator_deactivate'),
    url(r'^platters/$', core.views.PlatterListView.as_view(), name='platter_list'),
    url(r'^platters/create/$', core.views.PlatterCreateView.as_view(), name='platter_create'),
    url(r'^platters/(?P<id>\d+)/activate/$', never_cache(core.views.ActivatePlatterRedirectView.as_view()), name='platter_activate'),
    url(r'^platters/(?P<id>\d+)/deactivate/$', never_cache(core.views.DeactivatePlatterRedirectView.as_view()), name='platter_deactivate'),
    url(r'^projects/$', core.views.ProjectListView.as_view(), name='project_list'),
    url(r'^projects/create/$', core.views.ProjectCreateView.as_view(), name='project_create'),
    url(r'^projects/track/$', core.views.TrackProjectView.as_view(), name='track_project'),
    url(r'^projects/(?P<slug>[\w-]+)/$', core.views.ProjectDetailView.as_view(), name='project_detail_all'),
    url(r'^projects/(?P<slug>[\w-]+)/edit/$', core.views.ProjectUpdateView.as_view(), name='project_update'),
    url(r'^projects/(?P<slug>[\w-]+)/track/$', never_cache(core.views.TrackProjectRedirectView.as_view()), name='project_track'),
    url(r'^projects/(?P<slug>[\w-]+)/untrack/$', never_cache(core.views.UntrackProjectRedirectView.as_view()), name='project_untrack'),
    url(r'^projects/(?P<slug>[\w-]+)/activate/$', never_cache(core.views.ActivateProjectRedirectView.as_view()), name='project_activate'),
    url(r'^projects/(?P<slug>[\w-]+)/deactivate/$', never_cache(core.views.DeactivateProjectRedirectView.as_view()), name='project_deactivate'),
    url(r'^projects/(?P<slug>[\w-]+)/add-investigation/$', core.views.InvestigationCreateView.as_view(), name='investigation_create'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$', core.views.InvestigationDetailView.as_view(), name='investigation_detail_all'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/edit/$', core.views.InvestigationUpdateView.as_view(), name='investigation_update'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/activate/$', never_cache(core.views.ActivateInvestigationRedirectView.as_view()), name='investigation_activate'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/deactivate/$', never_cache(core.views.DeactivateInvestigationRedirectView.as_view()), name='investigation_deactivate'),
    url(r'^investigations/$', core.views.InvestigationListView.as_view(), name='investigation_list'),



    # growths urls
    url(r'^growths/search/$', login_required(growths.views.growth_list.as_view()), name='afm_filter'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', login_required(growths.views.GrowthDetailView.as_view()), name='growth_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/update$', login_required(growths.views.GrowthUpdateView.as_view()), name='growth_update'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/recipe/$', login_required(growths.views.recipe_detail.as_view()), name='recipe_detail'),
    url(r'^(?P<growth>[gt][1-9][0-9]{3,})/(?P<pocket>\d+\-?\d*)/$', login_required(growths.views.SampleFamilyDetailView.as_view()), name='sample_family_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/$', login_required(growths.views.readings_detail.as_view()), name='readings_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/update/$', login_required(growths.views.update_readings.as_view()), name='update_readings'),
    url(r'^sample/(?P<pk>\d+)/$', login_required(growths.views.SampleDetailView.as_view()), name='sample_detail'),
    url(r'^sample/split/$', login_required(growths.views.SplitSampleView.as_view()), name='split_sample'),

    # dashboard views
    url(r'^dashboard/', include('dashboard.urls')),

    # journal urls
    url(r'^notebook/', include('journal.urls')),

    # creategrowth urls
    url(r'^creategrowth/start/$', login_required(growths.views.CreateGrowthStartView.as_view()), name='create_growth_start'),
    url(r'^creategrowth/prerun/$', login_required(growths.views.CreateGrowthPrerunView.as_view()), name='create_growth_prerun'),
    url(r'^creategrowth/readings/$', login_required(growths.views.create_growth_readings.as_view()), name='create_growth_readings'),
    url(r'^creategrowth/postrun/$', login_required(growths.views.create_growth_postrun), name='create_growth_postrun'),

    # afm urls
    url(r'^afm/', include('afm.urls')),
    url(r'^api/v0/afm/$', afm.api.AFMListAPI.as_view()),
    url(r'^api/v0/afm/(?P<pk>\d+)/$', afm.api.AFMDetailAPI.as_view()),

    # hall urls
    url(r'^hall/$', include('hall.urls')),
    
    # user-specific views
    url(r'^(?P<username>[\w-]+)/(?P<slug>[\w-]+)/$', login_required(core.views.ProjectDetailView.as_view()), name='project_detail_user'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
