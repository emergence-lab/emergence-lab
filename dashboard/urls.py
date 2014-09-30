from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProjectDetailDashboardView.as_view(), name='project_detail_dashboard'),
    url(r'^(?P<project>[\w-]+)/(?P<slug>[\w-]+)/$', views.InvestigationDetailDashboardView.as_view(), name='investigation_detail_dashboard'),
]
