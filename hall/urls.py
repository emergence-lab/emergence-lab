from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.hall_list.as_view()), name='hall_list'),
    url(r'^(?P<pk>\d+)/$', login_required(views.hall_detail.as_view()), name='hall_detail'),
)
