from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.Dashboard.as_view()), name='dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', login_required(views.ProjectDetailDashboardView.as_view()), name='project_detail_dashboard'),
    url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$', login_required(views.InvestigationDetailDashboardView.as_view()), name='investigation_detail_dashboard'),
)
