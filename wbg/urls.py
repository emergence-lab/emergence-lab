from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

import core.views
import project_management.views


admin.autodiscover()

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^django-rq/', include('django_rq.urls')),

    # misc urls
    url(r'^$', core.views.HomepageView.as_view(), name='home'),
    url(r'^media/(?P<filename>.*)$', core.views.ProtectedMediaView.as_view()),
    url(r'^quicksearch/',
        core.views.QuickSearchRedirectView.as_view(), name='quicksearch'),
    url(r'^exception/',
        core.views.ExceptionHandlerView.as_view(), name='exception'),
    url(r'^accounts/login/',
        login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/',
        logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^accounts/', include('users.urls')),
    url(r'^wbg-admin/', include(admin.site.urls)),
    url(r'^about/', core.views.AboutView.as_view(), name='about'),

    # core urls
    url(r'^operators/$',
        core.views.UserListView.as_view(), name='operator_list'),
    url(r'^operators/(?P<id>\d+)/activate$',
        core.views.ActivateUserRedirectView.as_view(),
        name='operator_activate'),
    url(r'^operators/(?P<id>\d+)/deactivate$',
        core.views.DeactivateUserRedirectView.as_view(),
        name='operator_deactivate'),
    url(r'^projects/$',
        core.views.ProjectListView.as_view(), name='project_list'),
    url(r'^projects/create/$',
        core.views.ProjectCreateView.as_view(), name='project_create'),
    url(r'^projects/track/$',
        core.views.TrackProjectView.as_view(), name='track_project'),
    url(r'^projects/(?P<slug>[\w-]+)/$',
        core.views.ProjectDetailView.as_view(), name='project_detail_all'),
    url(r'^projects/(?P<slug>[\w-]+)/edit/$',
        core.views.ProjectUpdateView.as_view(), name='project_update'),
    url(r'^projects/(?P<slug>[\w-]+)/track/$',
        core.views.TrackProjectRedirectView.as_view(), name='project_track'),
    url(r'^projects/(?P<slug>[\w-]+)/untrack/$',
        core.views.UntrackProjectRedirectView.as_view(),
        name='project_untrack'),
    url(r'^projects/(?P<slug>[\w-]+)/activate/$',
        core.views.ActivateProjectRedirectView.as_view(),
        name='project_activate'),
    url(r'^projects/(?P<slug>[\w-]+)/deactivate/$',
        core.views.DeactivateProjectRedirectView.as_view(),
        name='project_deactivate'),
    url(r'^projects/(?P<slug>[\w-]+)/add-investigation/$',
        core.views.InvestigationCreateView.as_view(),
        name='investigation_create'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$',
        core.views.InvestigationDetailView.as_view(),
        name='investigation_detail_all'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/edit/$',
        core.views.InvestigationUpdateView.as_view(),
        name='investigation_update'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/activate/$',
        core.views.ActivateInvestigationRedirectView.as_view(),
        name='investigation_activate'),
    url(r'^projects/(?P<project>[\w-]+)/(?P<slug>[\w-]+)/deactivate/$',
        core.views.DeactivateInvestigationRedirectView.as_view(),
        name='investigation_deactivate'),
    url(r'^investigations/$',
        core.views.InvestigationListView.as_view(), name='investigation_list'),
    url(r'^samples/', include('core.urls.sample')),
    url(r'^process/', include('core.urls.process')),

    # afm urls
    url(r'^afm/', include('afm.urls')),

    # hall urls
    url(r'^hall/', include('hall.urls')),

    # API
    url(r'^api/', include('wbg.api')),

    # d180
    url(r'^d180/', include('d180.urls')),

    # # dashboard views
    url(r'^dashboard/', include('project_management.urls')),
    # url(r'^dashboard/', RedirectView.as_view(pattern_name='pm_landing')),

    # # journal urls
    url(r'^notebook/', include('journal.urls')),

    # simulation urls
    url(r'^simulations/', include('simulations.urls')),

    # schedule_queue urls
    url(r'^scheduling/', include('schedule_queue.urls')),

    # sem urls
    url(r'^sem/', include('sem.urls')),

    # print test
    url(r'^print/', core.views.utility.PrintTemplate.as_view(), name='print_test'),

    # project_management
    # url(r'^project_management/', include('project_management.urls')),
    url(r'^oauth$', project_management.views.MendeleyOAuth.as_view(), name='mendeley_oauth')
]

urlpatterns = format_suffix_patterns(urlpatterns)
