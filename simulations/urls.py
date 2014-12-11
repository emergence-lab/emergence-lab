from django.conf.urls import patterns, url
from simulations import views
from simulations import models
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^new/$', login_required(views.SimulationCreate.as_view()), name='create_form'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationEdit.as_view())), name='simulation_edit'),
    url(r'^cancel/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationCancel.as_view())), name='simulation_cancel'),
    url(r'^$', login_required(views.SimulationLanding.as_view()), name='simulation_landing'),
)