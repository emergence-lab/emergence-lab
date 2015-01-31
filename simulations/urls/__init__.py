from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from simulations import views


urlpatterns = [
    #url(r'^$', login_required(views.IncompleteSimulations.as_view()), name='simulation_incomplete'),
    #url(r'^new/$', login_required(views.SimulationCreate.as_view()), name='sim_create_form'),
    #url(r'^new/(?P<template_name>[a-z0-9\w-]+)$', login_required(never_cache(views.SimulationCreate.as_view())), name='sim_create_form_template'),
    #url(r'^duplicate/(?P<pk>\d+)$', login_required(never_cache(views.SimulationCreate.as_view())), name='sim_create_form_existing'),
    #url(r'^edit/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationEdit.as_view())), name='simulation_edit'),
    #url(r'^cancel/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationCancel.as_view())), name='simulation_cancel'),
    #url(r'^templates/$', login_required(never_cache(views.SimulationTemplates.as_view())), name='simulation_templates'),
    #url(r'^templates/create/$', login_required(never_cache(views.SimulationTemplateCreate.as_view())), name='simulation_template_create'),
    #url(r'^templates/create/(?P<pk>\d+)$', login_required(never_cache(views.SimulationJobToTemplate.as_view())), name='simulation_template_from_job'),
    #url(r'^templates/edit/(?P<template_name>[a-z0-9\w-]+)/$', login_required(never_cache(views.SimulationTemplateEdit.as_view())), name='simulation_template_edit'),
    #url(r'^templates/delete/(?P<template_name>[a-z0-9\w-]+)/$', login_required(never_cache(views.SimulationTemplateDelete.as_view())), name='simulation_template_delete'),
    #url(r'^completed/$', login_required(views.CompletedSimulations.as_view()), name='simulation_complete'),
    #url(r'^all/$', login_required(views.AllSimulations.as_view()), name='simulation_all'),
    url(r'^$', login_required(never_cache(views.SimulationAdmin.as_view())), name='simulation_admin'),
    url(r'^start_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(never_cache(views.StartInstance.as_view())), name='start_instance'),
    url(r'^stop_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(never_cache(views.StopInstance.as_view())), name='stop_instance'),
]
