from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.AFMList.as_view()), name='afm_list'),
    url(r'^create/$', login_required(views.AFMCreate.as_view()), name='afm_create'),
    url(r'^(?P<pk>\d+)/$', login_required(views.AFMDetail.as_view()), name='afm_detail'),
    url(r'^(?P<pk>\d+)/update/$', login_required(views.AFMUpdate.as_view()), name='afm_update'),
    url(r'^(?P<pk>\d+)/delete/$', login_required(views.AFMDelete.as_view()), name='afm_delete'),
)
