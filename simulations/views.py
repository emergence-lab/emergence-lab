from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.utils.timezone import activate
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import ListView, RedirectView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django import forms
from django.contrib.auth.models import User
from django.db import models
import datetime
import time

import aws_support as aws

from simulations.models import Simulation
from simulations.forms import SimInlineForm


class SimulationBase(ListView):
    model = Simulation
    template_name = 'simulations/management.html'
    paginate_by = 10


class IncompleteSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.filter(finish_date=None).order_by('id')

class CompletedSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.exclude(finish_date=None).order_by('-id')

class AllSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.order_by('-id')


class SimulationCreateSimple(CreateView):
    model = Simulation
    fields = ['priority', 'execution_node', 'file_path']
    template_name = 'simulations/create_form_simple.html'
    success_url = '/simulations'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('simulation_incomplete'))

class SimulationCreateInline(CreateView):
    model = Simulation
    form_class = SimInlineForm
    template_name = 'simulations/create_form_simple.html'
    success_url = '/simulations'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('simulation_incomplete'))

class SimulationCancel(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        simulation_obj = Simulation.objects.get(pk=pk)
        simulation_obj.delete()
        return reverse('simulation_incomplete')

class SimulationEdit(UpdateView):
    model = Simulation
    fields = ['priority', 'execution_node', 'file_path']
    template_name = 'simulations/edit_form.html'
    success_url = '/simulations'

class StartInstance(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.start_instance(instance)
            return reverse('simulation_admin')
        except Exception as e:
            raise Exception(e)

class StopInstance(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.stop_instance(instance)
            return reverse('simulation_admin')
        except Exception as e:
            raise Exception(e)

class SimulationAdmin(TemplateView):
    template_name = 'simulations/admin.html'

    signals = aws.EC2Connection(settings.AWS_EC2_REGION, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

    def get_context_data(self, **kwargs):
        tmp = []
        if 'instances' not in kwargs:
            for instance in self.signals.reservation_list()[0].instances:
                tmp.append({'instance_name': instance.id,
                            'instance_type': instance.instance_type,
                            'instance_state': instance.state,
                            'instance_uptime': self.signals.instance_uptime(instance.id)})
            kwargs['instances'] = tmp
        if 'status' not in kwargs:
            kwargs['status'] = self.signals.instance_list()[0].state
        return super(SimulationAdmin, self).get_context_data(**kwargs)
