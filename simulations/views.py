# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import ListView, RedirectView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.core.files.base import File
import os
import zipfile
import tempfile

import aws_support as aws

from simulations.models import Simulation
from simulations.forms import SimInlineForm, SimTemplateForm


class SimulationBase(ListView):
    model = Simulation
    template_name = 'simulations/management.html'
    paginate_by = 8


class IncompleteSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.filter(finish_date=None).order_by('id')


class CompletedSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.exclude(finish_date=None).order_by('-id')


class AllSimulations(SimulationBase):
    def get_queryset(self):
        return Simulation.objects.order_by('-id')


class SimulationCreate(CreateView):
    model = Simulation
    form_class = SimInlineForm
    template_name = 'simulations/sim_create_form.html'
    success_url = '/simulations'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(SimulationCreate, self).get_initial()

        try:
            s3_file_path = Simulation.objects.get(pk=self.kwargs['pk']).file_path.name
            zipdir = tempfile.mkdtemp()
            os.mkdir(os.path.join(zipdir, 'simulations'))
            original_file = zipfile.ZipFile(os.path.join(zipdir,
                                                         s3_file_path),
                                            'r')
            file_list = original_file.namelist()
            for item in file_list:
                if item.endswith('.par'):
                    initial['materials'] = original_file.read(item)
                if item.endswith('.scm'):
                    initial['device'] = original_file.read(item)
                if item.endswith('.cmd'):
                    initial['physics'] = original_file.read(item)
        except KeyError:
            try:
                base_path = os.path.join(settings.MEDIA_ROOT,
                                         'simulations',
                                         'templates',
                                         str(self.request.user),
                                         self.kwargs['template_name'])
            except KeyError:
                base_path = os.path.join(settings.MEDIA_ROOT,
                                         'simulations',
                                         'templates',
                                         'global',
                                         'default')
            initial['materials'] = open(os.path.join(base_path,
                                                     'materials.par')).read()
            initial['physics'] = open(os.path.join(base_path,
                                                     'physics.cmd')).read()
            initial['device'] = open(os.path.join(base_path,
                                                     'device.scm')).read()
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        zipdir = tempfile.mkdtemp()
        zipout = zipfile.ZipFile(os.path.join(zipdir,
                                              str(str(self.request.user)
                                                  + '.zip')),
                                     'w')
        if form.cleaned_data['materials_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.par', dir=zipdir).name,
                      'w+') as materials:
                for chunk in self.request.FILES['materials_upload'].chunks():
                    materials.write(chunk.encode('utf-8'))
                materials.seek(0)
                zipout.write(materials.name, os.path.basename(materials.name))
                materials.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.par', dir=zipdir).name,
                      'w+') as materials:
                materials.write(form.data['materials'].encode('utf-8'))
                materials.seek(0)
                zipout.write(materials.name, os.path.basename(materials.name))
                materials.close()
        if form.cleaned_data['device_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.scm', dir=zipdir).name,
                      'w+') as device:
                for chunk in self.request.FILES['device_upload'].chunks():
                    device.write(chunk.encode('utf-8'))
                device.seek(0)
                zipout.write(device.name, os.path.basename(device.name))
                device.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.scm', dir=zipdir).name,
                      'w+') as device:
                device.write(form.data['device'].encode('utf-8'))
                device.seek(0)
                zipout.write(device.name, os.path.basename(device.name))
                device.close()
        if form.cleaned_data['physics_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.cmd', dir=zipdir).name,
                      'w+') as physics:
                for chunk in self.request.FILES['physics_upload'].chunks():
                    physics.write(chunk.encode('utf-8'))
                physics.seek(0)
                zipout.write(physics.name, os.path.basename(physics.name))
                physics.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.cmd', dir=zipdir).name,
                      'w+') as physics:
                physics.write(form.data['physics'].encode('utf-8'))
                physics.seek(0)
                zipout.write(physics.name, os.path.basename(physics.name))
                physics.close()
        zipout.close()
        self.object.file_path = File(open(zipout.filename, 'rb'))
        self.object.user = self.request.user
        self.object = form.save()
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
    form_class = SimInlineForm
    template_name = 'simulations/edit_form.html'
    success_url = '/simulations'

    storage = aws.S3FileManager(settings.AWS_ACCESS_KEY_ID,
                                settings.AWS_SECRET_ACCESS_KEY,
                                True)
    zipdir = tempfile.mkdtemp()
    os.mkdir(os.path.join(zipdir, 'simulations'))

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(SimulationEdit, self).get_initial()
        original_file = zipfile.ZipFile(os.path.join(self.zipdir,
                                                     self.object.file_path.name),
                                        'r')
        self.file_list = original_file.namelist()
        for item in self.file_list:
            if item.endswith('.par'):
                initial['materials'] = original_file.read(item)
            if item.endswith('.scm'):
                initial['device'] = original_file.read(item)
            if item.endswith('.cmd'):
                initial['physics'] = original_file.read(item)
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        zipout = zipfile.ZipFile(os.path.join(self.zipdir,
                                              str(str(self.request.user)
                                                  + '.zip')),
                                     'w')
        if form.cleaned_data['materials_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.par', dir=self.zipdir).name,
                      'w+') as materials:
                for chunk in self.request.FILES['materials_upload'].chunks():
                    materials.write(chunk.encode('utf-8'))
                materials.seek(0)
                zipout.write(materials.name, os.path.basename(materials.name))
                materials.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.par', dir=self.zipdir).name,
                      'w+') as materials:
                materials.write(form.data['materials'].encode('utf-8'))
                materials.seek(0)
                zipout.write(materials.name, os.path.basename(materials.name))
                materials.close()
        if form.cleaned_data['device_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.scm', dir=self.zipdir).name,
                      'w+') as device:
                for chunk in self.request.FILES['device_upload'].chunks():
                    device.write(chunk.encode('utf-8'))
                device.seek(0)
                zipout.write(device.name, os.path.basename(device.name))
                device.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.scm', dir=self.zipdir).name,
                      'w+') as device:
                device.write(form.data['device'].encode('utf-8'))
                device.seek(0)
                zipout.write(device.name, os.path.basename(device.name))
                device.close()
        if form.cleaned_data['physics_upload']:
            with open(tempfile.NamedTemporaryFile(suffix='.cmd', dir=self.zipdir).name,
                      'w+') as physics:
                for chunk in self.request.FILES['physics_upload'].chunks():
                    physics.write(chunk.encode('utf-8'))
                physics.seek(0)
                zipout.write(physics.name, os.path.basename(physics.name))
                physics.close()
        else:
            with open(tempfile.NamedTemporaryFile(suffix='.cmd', dir=self.zipdir).name,
                      'w+') as physics:
                physics.write(form.data['physics'].encode('utf-8'))
                physics.seek(0)
                zipout.write(physics.name, os.path.basename(physics.name))
                physics.close()
        zipout.close()
        self.object.file_path = File(open(zipout.filename, 'rb'))
        self.object = form.save()
        return HttpResponseRedirect(reverse('simulation_incomplete'))


class StartInstance(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                    settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.start_instance(instance)
            return reverse('simulation_admin')
        except Exception as e:
            raise Exception(e)


class StopInstance(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                    settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.stop_instance(instance)
            return reverse('simulation_admin')
        except Exception as e:
            raise Exception(e)


class SimulationAdmin(TemplateView):
    template_name = 'simulations/admin.html'

    signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                settings.AWS_ACCESS_KEY_ID,
                                settings.AWS_SECRET_ACCESS_KEY)

    def get_context_data(self, **kwargs):
        tmp = []
        if 'instances' not in kwargs:
            for instance in self.signals.instance_list():
                tmp.append({'instance_name': instance.id,
                            'instance_type': instance.instance_type,
                            'instance_state': instance.state,
                            'instance_uptime': self.signals.instance_uptime(instance.id)})
            kwargs['instances'] = tmp
        return super(SimulationAdmin, self).get_context_data(**kwargs)


class SimulationTemplates(TemplateView):
    template_name = 'simulations/template_list.html'

    def get_context_data(self, **kwargs):
        user = str(self.request.user)
        tmp = []
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)):
            if 'template_list' not in kwargs:
                for template in os.listdir(os.path.join(settings.MEDIA_ROOT,
                                                        'simulations',
                                                        'templates',
                                                        user)):
                    if os.path.isdir(os.path.join(settings.MEDIA_ROOT,
                                                  'simulations',
                                                  'templates',
                                                  user,
                                                  template)):
                        if os.path.isfile(os.path.join(settings.MEDIA_ROOT,
                                                       'simulations',
                                                       'templates',
                                                       user,
                                                       template,
                                                       'comment.txt')):
                            with open(os.path.join(settings.MEDIA_ROOT,
                                                   'simulations',
                                                   'templates',
                                                   user,
                                                   template,
                                                   'comment.txt'), 'r') as f:
                                comment = f.read()
                        else:
                            comment = None
                        tmp.append({'name': template,
                                    'path': os.path.join(settings.MEDIA_ROOT,
                                                         'simulations',
                                                         'templates',
                                                         user,
                                                         template),
                                    'files': os.listdir(os.path.join(settings.MEDIA_ROOT,
                                                                     'simulations',
                                                                     'templates',
                                                                     user)),
                                    'comment': comment})
                kwargs['template_list'] = tmp
        return super(SimulationTemplates, self).get_context_data(**kwargs)


class SimulationTemplateDelete(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        template_name = kwargs.pop('template_name')
        user = str(self.request.user)
        try:
            for item in os.listdir(os.path.join(settings.MEDIA_ROOT,
                                                'simulations',
                                                'templates',
                                                user,
                                                template_name)):
                os.remove(os.path.join(settings.MEDIA_ROOT,
                                       'simulations',
                                       'templates',
                                       user,
                                       template_name,
                                       item))
            os.rmdir(os.path.join(settings.MEDIA_ROOT,
                                  'simulations',
                                  'templates',
                                  user,
                                  template_name))
            return reverse('simulation_templates')
        except Exception as e:
            raise Exception(e)


class SimulationTemplateCreate(FormView):
    form_class = SimTemplateForm
    template_name = 'simulations/template_form.html'
    success_url = '/simulations/templates/'

    def form_valid(self, form):
        user = str(self.request.user)
        base_path = os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)
        try:
            os.mkdir(os.path.join(base_path, form.cleaned_data['template_name']))
            base_path = os.path.join(base_path, form.cleaned_data['template_name'])
        except Exception as e:
            print(e)
        if form.cleaned_data['materials_upload']:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                for chunk in self.request.FILES['materials_upload'].chunks():
                    materials.write(chunk.encode('utf-8'))
                materials.close()
        else:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                materials.write(form.data['materials'].encode('utf-8'))
                materials.close()
        if form.cleaned_data['device_upload']:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                for chunk in self.request.FILES['device_upload'].chunks():
                    device.write(chunk.encode('utf-8'))
                device.close()
        else:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                device.write(form.data['device'].encode('utf-8'))
                device.close()
        if form.cleaned_data['physics_upload']:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                for chunk in self.request.FILES['physics_upload'].chunks():
                    physics.write(chunk.encode('utf-8'))
                physics.close()
        else:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                physics.write(form.data['physics'].encode('utf-8'))
                physics.close()
        if form.cleaned_data['comment']:
            with open(os.path.join(base_path, 'comment.txt'), 'w+') as comment:
                comment.write(form.cleaned_data['comment'])
                comment.close()
        return HttpResponseRedirect(reverse('simulation_templates'))


class SimulationTemplateEdit(FormView):
    form_class = SimTemplateForm
    template_name = 'simulations/template_form.html'
    success_url = '/simulations/templates/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(SimulationTemplateEdit, self).get_initial()
        initial['template_name'] = self.kwargs['template_name']
        template_path = os.path.join(settings.MEDIA_ROOT,
                                     'simulations',
                                     'templates',
                                     str(self.request.user),
                                     self.kwargs['template_name'])
        self.file_list = os.listdir(template_path)
        try:
            for item in self.file_list:
                if item == 'materials.par':
                    initial['materials'] = open(os.path.join(template_path, item)).read()
                if item == 'device.scm':
                    initial['device'] = open(os.path.join(template_path, item)).read()
                if item == 'physics.cmd':
                    initial['physics'] = open(os.path.join(template_path, item)).read()
                if item == 'comments.txt':
                    initial['comment'] = open(os.path.join(template_path, item)).read()
        except Exception as e:
            print(e)
        initial['template_name'] = self.kwargs['template_name']
        return initial

    def form_valid(self, form):
        user = str(self.request.user)
        base_path = os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)
        try:
            base_path = os.path.join(base_path, form.cleaned_data['template_name'])
        except Exception as e:
            print(e)
        if form.cleaned_data['materials_upload']:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                materials.truncate()
                materials.seek(0)
                for chunk in self.request.FILES['materials_upload'].chunks():
                    materials.write(chunk.encode('utf-8'))
                materials.close()
        else:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                materials.truncate()
                materials.seek(0)
                materials.write(form.data['materials'].encode('utf-8'))
                materials.close()
        if form.cleaned_data['device_upload']:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                device.truncate()
                device.seek(0)
                for chunk in self.request.FILES['device_upload'].chunks():
                    device.write(chunk.encode('utf-8'))
                device.close()
        else:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                device.truncate()
                device.seek(0)
                device.write(form.data['device'].encode('utf-8'))
                device.close()
        if form.cleaned_data['physics_upload']:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                physics.truncate()
                physics.seek(0)
                for chunk in self.request.FILES['physics_upload'].chunks():
                    physics.write(chunk.encode('utf-8'))
                physics.close()
        else:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                physics.truncate()
                physics.seek(0)
                physics.write(form.data['physics'].encode('utf-8'))
                physics.close()
        if form.cleaned_data['comment']:
            with open(os.path.join(base_path, 'comment.txt'), 'w+') as comment:
                comment.truncate()
                comment.seek(0)
                comment.write(form.cleaned_data['comment'])
                comment.close()
        return HttpResponseRedirect(reverse('simulation_templates'))


class SimulationJobToTemplate(FormView):
    model = Simulation
    form_class = SimTemplateForm
    template_name = 'simulations/template_form.html'
    success_url = '/simulations/templates'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(SimulationJobToTemplate, self).get_initial()
        try:
            s3_file_path = Simulation.objects.get(pk=self.kwargs['pk']).file_path.name
            zipdir = tempfile.mkdtemp()
            os.mkdir(os.path.join(zipdir, 'simulations'))
            original_file = zipfile.ZipFile(os.path.join(zipdir,
                                                         s3_file_path),
                                            'r')
            file_list = original_file.namelist()
            for item in file_list:
                if item.endswith('.par'):
                    initial['materials'] = original_file.read(item)
                if item.endswith('.scm'):
                    initial['device'] = original_file.read(item)
                if item.endswith('.cmd'):
                    initial['physics'] = original_file.read(item)
        except Exception as e:
            print(e)
        return initial

    def form_valid(self, form):
        user = str(self.request.user)
        base_path = os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)
        try:
            base_path = os.path.join(base_path, form.cleaned_data['template_name'])
        except Exception as e:
            print(e)
        if form.cleaned_data['materials_upload']:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                materials.truncate()
                materials.seek(0)
                for chunk in self.request.FILES['materials_upload'].chunks():
                    materials.write(chunk.encode('utf-8'))
                materials.close()
        else:
            with open(os.path.join(base_path, 'materials.par'), 'w+') as materials:
                materials.truncate()
                materials.seek(0)
                materials.write(form.data['materials'].encode('utf-8'))
                materials.close()
        if form.cleaned_data['device_upload']:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                device.truncate()
                device.seek(0)
                for chunk in self.request.FILES['device_upload'].chunks():
                    device.write(chunk.encode('utf-8'))
                device.close()
        else:
            with open(os.path.join(base_path, 'device.scm'), 'w+') as device:
                device.truncate()
                device.seek(0)
                device.write(form.data['device'].encode('utf-8'))
                device.close()
        if form.cleaned_data['physics_upload']:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                physics.truncate()
                physics.seek(0)
                for chunk in self.request.FILES['physics_upload'].chunks():
                    physics.write(chunk.encode('utf-8'))
                physics.close()
        else:
            with open(os.path.join(base_path, 'physics.cmd'), 'w+') as physics:
                physics.truncate()
                physics.seek(0)
                physics.write(form.data['physics'].encode('utf-8'))
                physics.close()
        if form.cleaned_data['comment']:
            with open(os.path.join(base_path, 'comment.txt'), 'w+') as comment:
                comment.truncate()
                comment.seek(0)
                comment.write(form.cleaned_data['comment'])
                comment.close()
        return HttpResponseRedirect(reverse('simulation_templates'))
