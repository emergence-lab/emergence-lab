from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.utils.timezone import activate
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django import forms
from django.contrib.auth.models import User
from django.db import models
import datetime
import time

from simulations.models import Simulation
from simulations.aws_simulations import ec2_metal_ops as metal

class SimulationLanding(ListView):
    model = Simulation
    queryset = Simulation.objects.all()
    template_name = 'simulations/landing.html'
    
    signals = metal.EC2_Connection(settings.AWS_EC2_REGION, settings.AWS_EC2_KEY, settings.AWS_EC2_SECRET)
    
    def get_context_data(self, **kwargs):
        tmp = []
        if 'instances' not in kwargs:
            for instance in self.signals.reservation_list()[0].instances:
                tmp.append({'instance_name': instance.id,
                            'instance_type': instance.instance_type,
                            'instance_state': instance.state})
            kwargs['instances'] = tmp
        if 'status' not in kwargs:
            kwargs['status'] = self.signals.instance_list()[0].state
        return super(SimulationLanding, self).get_context_data(**kwargs)
    
    def get_queryset(self):
        return Simulation.objects.exclude(completed=True).order_by('id')
    
    def index(request):
        return HttpResponse(queryset)
    
class SimulationCreate(CreateView):
    model = Simulation
    fields = ['priority', 'execution_node', 'input_file_path', 'output_file_path']
    template_name = 'simulations/create_form.html'
    success_url = '/simulations'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('simulation_landing'))
    
class SimulationCancel(RedirectView):
    permanent = False  
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        simulation_obj = Simulation.objects.get(pk=pk)
        if not simulation_obj.completed:
            simulation_obj.completed = True
            simulation_obj.save()
        return reverse('simulation_landing')

class SimulationEdit(UpdateView):
    model = Simulation
    fields = ['priority', 'execution_node', 'input_file_path', 'output_file_path']
    template_name = 'simulations/edit_form.html'
    success_url = '/simulations'

class SimulationManagement(ListView):
    model = Simulation
    queryset = Simulation.objects.all()
    template_name = 'simulations/management.html'
    
    signals = metal.EC2_Connection(settings.AWS_EC2_REGION, settings.AWS_EC2_KEY, settings.AWS_EC2_SECRET)
    
    def get_context_data(self, **kwargs):
        tmp = []
        if 'instances' not in kwargs:
            for instance in self.signals.reservation_list()[0].instances:
                tmp.append({'instance_name': instance.id,
                            'instance_type': instance.instance_type,
                            'instance_state': instance.state,
                            #'instance_launchtime': datetime.datetime.fromtimestamp(\
                            #    time.mktime(time.strptime(instance.launch_time.split('.')[0],
                            #                              "%Y-%m-%dT%H:%M:%S")))
                            'instance_uptime': self.signals.instance_uptime(instance.id)})
            kwargs['instances'] = tmp
        if 'status' not in kwargs:
            kwargs['status'] = self.signals.instance_list()[0].state
        return super(SimulationManagement, self).get_context_data(**kwargs)
    
    def get_queryset(self):
        #return Simulation.objects.exclude(completed=True).order_by('id')
        return Simulation.objects.order_by('-id')
    
    def index(request):
        return HttpResponse(queryset)
   
class StartInstance(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        signals = metal.EC2_Connection(settings.AWS_EC2_REGION, settings.AWS_EC2_KEY, settings.AWS_EC2_SECRET)
        instance = kwargs.pop('instance_id')
        try:
            signals.start_instance(instance)
            return reverse('simulation_management')
        except Exception as e:
            raise Exception(e)
    
class StopInstance(RedirectView):
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        signals = metal.EC2_Connection(settings.AWS_EC2_REGION, settings.AWS_EC2_KEY, settings.AWS_EC2_SECRET)
        instance = kwargs.pop('instance_id')
        try:
            signals.stop_instance(instance)
            return reverse('simulation_management')
        except Exception as e:
            raise Exception(e)
