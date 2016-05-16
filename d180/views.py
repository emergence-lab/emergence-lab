# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from d180.models import D180Source, D180Readings, Platter
from d180.forms import (CommentsForm, SourcesForm,
                        WizardBasicProcessForm, WizardGrowthInfoForm, WizardFullProcessForm,
                        WizardPrerunChecklistForm, WizardPostrunChecklistForm,
                        D180ReadingsFormSet, ReservationCloseForm,
                        D180ReadingsForm)
from core.views import ActionReloadView, ActiveListView
from core.forms import SampleFormSet
from core.models import Process, ProcessTemplate, ProcessType
from schedule_queue.models import Reservation


logger = logging.getLogger('emergence.process.d180')


class PlatterListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "d180/platter_list.html"
    model = Platter


class PlatterCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a platter.
    """
    template_name = 'd180/platter_create.html'
    model = Platter
    fields = ('name', 'serial',)

    def form_valid(self, form):
        form.instance.is_active = True
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('platter_list')


class ActivatePlatterReloadView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified platter to active.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        platter = Platter.objects.get(pk=pk)
        platter.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('platter_list')


class DeactivatePlatterReloadView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified platter to inactive.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        platter = Platter.objects.get(pk=pk)
        platter.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('platter_list')


class WizardStartView(LoginRequiredMixin, generic.TemplateView):
    """
    Steps through creating a growth.
    """
    template_name = 'd180/create_growth_start.html'

    def build_forms(self):
        try:
            previous_source = D180Source.objects.latest('created')
        except ObjectDoesNotExist:
            previous_source = None

        try:
            previous_growth = (Process.objects.filter(type_id='d180-growth')
                                              .latest('created'))
            growth_number = 'g{}'.format(
                str(int(previous_growth.legacy_identifier[1:]) + 1).zfill(4))
        except ObjectDoesNotExist:
            growth_number = 'g1000'
        except ValueError:
            growth_number = 'g1000'

        return {
            'info_form': WizardBasicProcessForm(
                initial={
                    'user': self.request.user,
                    'legacy_identifier': growth_number,
                    'type': ProcessType.objects.get(type='d180-growth'),
                },
                user=self.request.user,
                prefix='process'),
            'growth_form': WizardGrowthInfoForm(prefix='growth'),
            'checklist_form': WizardPrerunChecklistForm(prefix='checklist'),
            'source_form': SourcesForm(instance=previous_source,
                                       prefix='source'),
            'comment_form': CommentsForm(prefix='process'),
            'sample_formset': SampleFormSet(prefix='sample'),
            'reservation_form': ReservationCloseForm(prefix='reservation'),
        }

    def get(self, request, *args, **kwargs):
        self.object = None
        reservation = Reservation.get_latest(user=self.request.user,
                                             process_type='d180-growth')
        return self.render_to_response(self.get_context_data(
            reservation=reservation, **self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = None
        process_form = WizardFullProcessForm(request.POST, prefix='process')
        growth_info_form = WizardGrowthInfoForm(request.POST, prefix='growth')
        checklist_form = WizardPrerunChecklistForm(request.POST,
                                                   prefix='checklist')
        source_form = SourcesForm(request.POST, prefix='source')
        sample_formset = SampleFormSet(request.POST, prefix='sample')
        reservation_form = ReservationCloseForm(request.POST, prefix='reservation')

        if all([process_form.is_valid(), growth_info_form.is_valid(),
                source_form.is_valid(), checklist_form.is_valid(),
                sample_formset.is_valid(), reservation_form.is_valid()]):
            logger.debug('Creating new growth')
            self.object = process_form.save()
            info = growth_info_form.save(commit=False)
            info.process = self.object
            info.save()
            logger.debug('Created process {} ({}) for {} samples'.format(
                self.object.uuid_full, self.object.legacy_identifier, len(sample_formset)))
            source_form.save()
            for n, s in enumerate(sample_formset):
                sample = s.save()
                logger.debug('Created sample {}'.format(sample.uuid))
                piece = s.cleaned_data['piece']
                sample.run_process(self.object, piece, n + 1)
            reservation = Reservation.get_latest(user=self.request.user,
                                                 process_type=self.object.type)
            if reservation and not reservation_form.cleaned_data['hold_open']:
                reservation.deactivate()

            return HttpResponseRedirect(reverse('create_growth_d180_readings'))
        else:
            process_form = WizardBasicProcessForm(self.request.user, request.POST,
                                                    prefix='process')
            growth_info_form = WizardGrowthInfoForm(request.POST, prefix='growth')
            comment_form = CommentsForm(request.POST, prefix='process')
            return self.render_to_response(self.get_context_data(
                info_form=process_form,
                growth_form=growth_info_form,
                checklist_form=checklist_form,
                source_form=source_form,
                comment_form=comment_form,
                sample_formset=sample_formset,
                reservation_form=reservation_form,
                reservation=Reservation.get_latest(user=self.request.user,
                                                   process_type='d180-growth')))


class WizardReadingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'd180/create_growth_readings.html'

    def get_object(self):
        return Process.objects.filter(type_id='d180-growth').latest('created')

    def build_forms(self, **kwargs):
        comment_form = CommentsForm(prefix='comment',
                                    initial={'title': self.object.title,
                                             'comment': self.object.comment})
        readings = self.object.readings.get_queryset()
        readings_formset = D180ReadingsFormSet(queryset=readings,
                                               prefix='reading')
        return {
            'comment_form': comment_form,
            'readings_formset': readings_formset,
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data(**self.build_forms()))

    def get_context_data(self, **kwargs):
        context_data = super(WizardReadingsView, self).get_context_data(**kwargs)
        context_data['growth'] = self.object
        nodes = self.object.nodes.order_by('number')
        context_data['sample_info'] = zip([n.get_sample() for n in nodes], nodes)
        return context_data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentsForm(request.POST, prefix='comment')
        readings = self.object.readings.get_queryset()
        readings_formset = D180ReadingsFormSet(request.POST, queryset=readings,
                                               prefix='reading')

        if comment_form.is_valid() and readings_formset.is_valid():
            if comment_form.has_changed():
                self.object.comment = comment_form.cleaned_data['comment']
                self.object.title = comment_form.cleaned_data['title']
                self.object.save()
            for reading_form in readings_formset:
                if reading_form.has_changed():
                    reading_form.save(process=self.object)
            return HttpResponseRedirect(reverse('create_growth_d180_readings'))
        else:
            return self.render_to_response(self.get_context_data(
                comment_form=comment_form,
                readings_formset=readings_formset,
            ))


class WizardPostrunView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'd180/create_growth_postrun.html'

    def get_object(self):
        return Process.objects.filter(type_id='d180-growth').latest('created')

    def build_forms(self):
        try:
            previous_source = D180Source.objects.latest('created')
        except ObjectDoesNotExist:
            previous_source = None

        comment_form = CommentsForm(prefix='comment',
                                    initial={'title': self.object.title,
                                             'comment': self.object.comment})
        return {
            'checklist_form': WizardPostrunChecklistForm(prefix='checklist'),
            'source_form': SourcesForm(instance=previous_source,
                                       prefix='source'),
            'comment_form': comment_form,
        }

    def get_context_data(self, **kwargs):
        context_data = super(WizardPostrunView, self).get_context_data(**kwargs)
        context_data['growth'] = self.object
        nodes = self.object.nodes.order_by('number')
        context_data['sample_info'] = zip([n.get_sample() for n in nodes], nodes)
        return context_data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data(**self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        checklist_form = WizardPostrunChecklistForm(request.POST,
                                                    prefix='checklist')
        source_form = SourcesForm(request.POST, prefix='source')
        comment_form = CommentsForm(request.POST, prefix='comment')

        if all([comment_form.is_valid(), source_form.is_valid(),
                checklist_form.is_valid()]):
            self.object.comment = comment_form.cleaned_data['comment']
            self.object.title = comment_form.cleaned_data['title']
            self.object.save()
            source_form.save()
            return HttpResponseRedirect(reverse('process_detail', args=(self.object.uuid,)))
        else:
            return self.render_to_response(self.get_context_data(
                checklist_form=checklist_form,
                source_form=source_form,
                comment_form=comment_form))


class WizardCancelView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        growth = Process.objects.filter(type_id='d180-growth').latest('created')

        # remove readings
        growth.readings.all().delete()
        # remove investigations from many-to-many
        for investigation in growth.investigations.all():
            growth.investigations.remove(investigation)
        # delete process node, removes all child nodes but there should be none
        for node in growth.nodes:
            node.delete()

        growth.delete()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard')


class ReadingsDetailView(LoginRequiredMixin, generic.ListView):
    model = D180Readings
    template_name = 'd180/readings_detail.html'
    context_object_name = 'readings'

    def get_queryset(self):
        uuid = Process.strip_uuid(self.kwargs['uuid'])
        try:
            self.process = Process.objects.get(uuid_full__startswith=uuid)
        except Process.DoesNotExist:
            raise Http404('Process {} does not exist'.format(self.kwargs['uuid']))
        return self.model.objects.filter(process=self.process).order_by('layer')

    def get_context_data(self, **kwargs):
        context = super(ReadingsDetailView, self).get_context_data(**kwargs)
        context['process'] = self.process

        readings_list = self.object_list.values_list()

        def molar_flow(temp, flow, press, a, b):
            if press <= 0:
                return 0.0
            vapor_press = 10 ** (a - b / (temp + 273))
            return (flow * vapor_press) / (press * 22400)

        converted_readings = [list(l) for l in readings_list]

        for n, readings in enumerate(converted_readings):
            tmga_molar = molar_flow(0, float(readings[29]), float(readings[30]), 8.07, 1703)
            tmga2_molar = molar_flow(0, float(readings[31]), float(readings[32]), 8.07, 1703)
            tega_molar = molar_flow(18, float(readings[33]), float(readings[34]), 8.083, 2152)
            tmin_molar = molar_flow(20, float(readings[35]), float(readings[36]), 10.52, 3014)
            tmal_molar = molar_flow(18, float(readings[37]), float(readings[38]), 8.224, 2135)
            aklyl_molar = tmga_molar + tmga2_molar + tega_molar + tmin_molar + tmal_molar

            nh3_molar = float(readings[27]) / 22400
            if aklyl_molar <= 0:
                viii_ratio = 0
            else:
                viii_ratio = nh3_molar / aklyl_molar

            readings.insert(39, round(tmal_molar * 10 ** 6, 2))
            readings.insert(37, round(tmin_molar * 10 ** 6, 2))
            readings.insert(35, round(tega_molar * 10 ** 6, 2))
            readings.insert(33, round(tmga2_molar * 10 ** 6, 2))
            readings.insert(31, round(tmga_molar * 10 ** 6, 2))
            readings.insert(29, round(viii_ratio, 2))
            readings.insert(29, round(nh3_molar * 10 ** 3, 2))

        context['readings_table'] = list(zip(
            ['ID', 'Growth ID', 'Layer', 'Description', 'Pyro Out', 'Pyro In', 'ECP Temp',
             'Thermocouple Out', 'Thermocouple In', 'Motor RPM', 'GC Pressure',
             'GC Position', 'Voltage In', 'Voltage Out', 'Current In',
             'Current Out', 'Top VP Flow', 'Hydride Inner', 'Hydride Outer',
             'Alkyl Flow Inner', 'Alkyl Push Inner', 'Alkyl Flow Middle',
             'Alkyl Push Middle', 'Alkyl Flow Outer', 'Alkyl Push Outer',
             'N2 Flow', 'H2 Flow', 'NH3 Flow', 'Hydride Pressure', 'NH3 Molar Flow', 'V/III Ratio',
             'TMGa1 Flow', 'TMGa1 Pressure', 'TMGa1 Molar Flow',
             'TMGa2 Flow', 'TMGa2 Pressure', 'TMGa2 Molar Flow',
             'TEGa1 Flow', 'TEGa1 Pressure', 'TEGa Molar Flow',
             'TMIn1 Flow', 'TMIn1 Pressure', 'TMIn Molar Flow',
             'TMAl1 Flow', 'TMAl1 Pressure', 'TMAl Molar Flow',
             'Cp2Mg Flow', 'Cp2Mg Pressure', 'Cp2Mg Dilution',
             'SiH4 Flow', 'SiH4 Dilution', 'SiH4 Mix', 'SiH4 Pressure'], *converted_readings))[2:]

        return context


class UpdateReadingsView(LoginRequiredMixin, generic.detail.SingleObjectMixin,
                         generic.TemplateView):
    context_object_name = 'growth'
    queryset = Process.objects.filter(type_id='d180-growth')
    template_name = 'd180/update_readings.html'

    def get_object(self):
        uuid = Process.strip_uuid(self.kwargs['uuid'])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(UpdateReadingsView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context["growth"] = self.object
        allreadings = D180Readings.objects.filter(process=self.object).order_by('layer')
        context["readings"] = allreadings
        formlist = []
        numberofreadings = 0
        for reading in allreadings:
            numberofreadings = numberofreadings + 1
            rform = D180ReadingsForm(instance=D180Readings(),
                                     prefix=('reading' + str(numberofreadings)),
                                     initial={'growth': reading.process,
                'layer': reading.layer, 'description': reading.description,
                'pyro_out': reading.pyro_out, 'pyro_in': reading.pyro_in,
                'ecp_temp': reading.ecp_temp, 'tc_out': reading.tc_out,
                'tc_in': reading.tc_in, 'motor_rpm': reading.motor_rpm,
                'gc_pressure': reading.gc_pressure, 'gc_position': reading.gc_position,
                'voltage_in': reading.voltage_in,
                'voltage_out': reading.voltage_out, 'current_in': reading.current_in,
                'current_out': reading.current_out, 'top_vp_flow': reading.top_vp_flow,
                'hydride_inner': reading.hydride_inner, 'hydride_outer': reading.hydride_outer,
                'alkyl_flow_inner': reading.alkyl_flow_inner,
                'alkyl_push_inner': reading.alkyl_push_inner,
                'alkyl_flow_middle': reading.alkyl_flow_middle,
                'alkyl_push_middle': reading.alkyl_push_middle,
                'alkyl_flow_outer': reading.alkyl_flow_outer,
                'alkyl_push_outer': reading.alkyl_push_outer,
                'n2_flow': reading.n2_flow, 'h2_flow': reading.h2_flow,
                'nh3_flow': reading.nh3_flow, 'hydride_pressure': reading.hydride_pressure,
                'tmga1_flow': reading.tmga1_flow, 'tmga1_pressure': reading.tmga1_pressure,
                'tmga2_flow': reading.tmga2_flow, 'tmga2_pressure': reading.tmga2_pressure,
                'tega2_flow': reading.tega2_flow, 'tega2_pressure': reading.tega2_pressure,
                'tmin1_flow': reading.tmin1_flow, 'tmin1_pressure': reading.tmin1_pressure,
                'tmal1_flow': reading.tmal1_flow, 'tmal1_pressure': reading.tmal1_pressure,
                'cp2mg_flow': reading.cp2mg_flow, 'cp2mg_pressure': reading.cp2mg_pressure,
                'cp2mg_dilution': reading.cp2mg_dilution, 'silane_flow': reading.silane_flow,
                'silane_dilution': reading.silane_dilution, 'silane_mix': reading.silane_mix,
                'silane_pressure': reading.silane_pressure})
            formlist.append(rform)
        context["readingslist"] = formlist
        return context

    def post(self, request, **kwargs):
        numberofreadings = len(D180Readings.objects.filter(process=self.get_object()))
        print (numberofreadings)
        for x in range(0, numberofreadings):
            rform = D180ReadingsForm(request.POST, prefix=('reading' + str(x + 1)))
            if rform.is_valid():
                newgrowth = self.get_object()
                newlayer = rform.cleaned_data['layer']
                newlayer_desc = rform.cleaned_data['description']
                newpyro_out = rform.cleaned_data['pyro_out']
                newpyro_in = rform.cleaned_data['pyro_in']
                newecp_temp = rform.cleaned_data['ecp_temp']
                newtc_out = rform.cleaned_data['tc_out']
                newtc_in = rform.cleaned_data['tc_in']
                newmotor_rpm = rform.cleaned_data['motor_rpm']
                newgc_pressure = rform.cleaned_data['gc_pressure']
                newgc_position = rform.cleaned_data['gc_position']
                newvoltage_in = rform.cleaned_data['voltage_in']
                newvoltage_out = rform.cleaned_data['voltage_out']
                newcurrent_in = rform.cleaned_data['current_in']
                newcurrent_out = rform.cleaned_data['current_out']
                newtop_vp_flow = rform.cleaned_data['top_vp_flow']
                newhydride_inner = rform.cleaned_data['hydride_inner']
                newhydride_outer = rform.cleaned_data['hydride_outer']
                newalkyl_flow_inner = rform.cleaned_data['alkyl_flow_inner']
                newalkyl_push_inner = rform.cleaned_data['alkyl_push_inner']
                newalkyl_flow_middle = rform.cleaned_data['alkyl_flow_middle']
                newalkyl_push_middle = rform.cleaned_data['alkyl_push_middle']
                newalkyl_flow_outer = rform.cleaned_data['alkyl_flow_outer']
                newalkyl_push_outer = rform.cleaned_data['alkyl_push_outer']
                newn2_flow = rform.cleaned_data['n2_flow']
                newh2_flow = rform.cleaned_data['h2_flow']
                newnh3_flow = rform.cleaned_data['nh3_flow']
                newhydride_pressure = rform.cleaned_data['hydride_pressure']
                newtmga1_flow = rform.cleaned_data['tmga1_flow']
                newtmga1_pressure = rform.cleaned_data['tmga1_pressure']
                newtmga2_flow = rform.cleaned_data['tmga2_flow']
                newtmga2_pressure = rform.cleaned_data['tmga2_pressure']
                newtega2_flow = rform.cleaned_data['tega2_flow']
                newtega2_pressure = rform.cleaned_data['tega2_pressure']
                newtmin1_flow = rform.cleaned_data['tmin1_flow']
                newtmin1_pressure = rform.cleaned_data['tmin1_pressure']
                newtmal1_flow = rform.cleaned_data['tmal1_flow']
                newtmal1_pressure = rform.cleaned_data['tmal1_pressure']
                newcp2mg_flow = rform.cleaned_data['cp2mg_flow']
                newcp2mg_pressure = rform.cleaned_data['cp2mg_pressure']
                newcp2mg_dilution = rform.cleaned_data['cp2mg_dilution']
                newsilane_flow = rform.cleaned_data['silane_flow']
                newsilane_dilution = rform.cleaned_data['silane_dilution']
                newsilane_mix = rform.cleaned_data['silane_mix']
                newsilane_pressure = rform.cleaned_data['silane_pressure']
                thisreading = D180Readings.objects.filter(process=newgrowth, layer=newlayer)
                thisreading.update(process=newgrowth, layer=newlayer,
                                   description=newlayer_desc, pyro_out=newpyro_out,
                                   pyro_in=newpyro_in, ecp_temp=newecp_temp,
                                   tc_out=newtc_out, tc_in=newtc_in, motor_rpm=newmotor_rpm,
                                   gc_pressure=newgc_pressure, gc_position=newgc_position,
                                   voltage_in=newvoltage_in, voltage_out=newvoltage_out,
                                   current_in=newcurrent_in, current_out=newcurrent_out,
                                   top_vp_flow=newtop_vp_flow, hydride_inner=newhydride_inner,
                                   hydride_outer=newhydride_outer,
                                   alkyl_flow_inner=newalkyl_flow_inner,
                                   alkyl_push_inner=newalkyl_push_inner,
                                   alkyl_flow_middle=newalkyl_flow_middle,
                                   alkyl_push_middle=newalkyl_push_middle,
                                   alkyl_flow_outer=newalkyl_flow_outer,
                                   alkyl_push_outer=newalkyl_push_outer,
                                   n2_flow=newn2_flow, h2_flow=newh2_flow,
                                   nh3_flow=newnh3_flow, hydride_pressure=newhydride_pressure,
                                   tmga1_flow=newtmga1_flow, tmga1_pressure=newtmga1_pressure,
                                   tmga2_flow=newtmga2_flow, tmga2_pressure=newtmga2_pressure,
                                   tega2_flow=newtega2_flow, tega2_pressure=newtega2_pressure,
                                   tmin1_flow=newtmin1_flow, tmin1_pressure=newtmin1_pressure,
                                   tmal1_flow=newtmal1_flow, tmal1_pressure=newtmal1_pressure,
                                   cp2mg_flow=newcp2mg_flow, cp2mg_pressure=newcp2mg_pressure,
                                   cp2mg_dilution=newcp2mg_dilution, silane_flow=newsilane_flow,
                                   silane_dilution=newsilane_dilution, silane_mix=newsilane_mix,
                                   silane_pressure=newsilane_pressure)
        return HttpResponseRedirect(reverse('d180_readings_edit', args=[self.get_object()]))


class TemplateWizardStartView(WizardStartView):

    def build_forms(self):
        if 'id' in self.kwargs:
            comment = ProcessTemplate.objects.get(id=self.kwargs.get('id', None)).comment
            process = ProcessTemplate.objects.get(id=self.kwargs.get('id', None)).process
        elif 'uuid' in self.kwargs:
            process = Process.objects.get(
                uuid_full__startswith=Process.strip_uuid(self.kwargs.get('uuid', None)))
            comment = process.comment
        output = super(TemplateWizardStartView, self).build_forms()
        output['comment_form'] = CommentsForm(initial={'comment': comment}, prefix='process')
        growth_info = {attr: getattr(process.info, attr)
                       for attr in WizardGrowthInfoForm.Meta.fields}
        output['growth_form'] = WizardGrowthInfoForm(initial=growth_info, prefix='growth')
        return output
