from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

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

    url(r'^projects/', include('core.urls.project')),


    # sample/process urls
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

    url(r'^oauth$', project_management.views.MendeleyOAuth.as_view(), name='mendeley_oauth')
]

urlpatterns = format_suffix_patterns(urlpatterns)
