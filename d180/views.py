# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import LoginRequiredMixin

from .models import D180Growth, D180Source, Platter
from .forms import (CommentsForm, SourcesForm, WizardBasicInfoForm,
                    WizardGrowthInfoForm, WizardFullForm,
                    WizardPrerunChecklistForm, WizardPostrunChecklistForm,
                    D180ReadingsFormSet, ReservationCloseForm)
from core.views import ActionReloadView, ActiveListView
from core.forms import SampleFormSet
from core.models import Sample

from schedule_queue.models import Reservation


class PlatterListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "growths/platter_list.html"
    model = Platter


class PlatterCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a platter.
    """
    template_name = 'growths/platter_create.html'
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
    template_name = 'growths/create_growth_start.html'

    def build_forms(self):
        try:
            previous_source = D180Source.objects.latest('created')
        except ObjectDoesNotExist:
            previous_source = None

        try:
            previous_growth = D180Growth.objects.latest('created')
            growth_number = 'g{}'.format(
                str(int(previous_growth.growth_number[1:]) + 1).zfill(4))
        except ObjectDoesNotExist:
            growth_number = 'g1000'
        except ValueError:
            growth_number = 'g1000'

        return {
            'info_form': WizardBasicInfoForm(
                initial={
                    'user': self.request.user,
                    'growth_number': growth_number
                },
                prefix='growth'),
            'growth_form': WizardGrowthInfoForm(prefix='growth'),
            'checklist_form': WizardPrerunChecklistForm(prefix='checklist'),
            'source_form': SourcesForm(instance=previous_source,
                                       prefix='source'),
            'comment_form': CommentsForm(prefix='growth'),
            'sample_formset': SampleFormSet(prefix='sample'),
            'reservation_form': ReservationCloseForm(prefix='reservation'),
        }

    def get(self, request, *args, **kwargs):
        self.object = None
        reservation = Reservation.get_latest(user=self.request.user, tool_name='d180')
        return self.render_to_response(self.get_context_data(reservation_object=reservation,
                                                             **self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = None
        growth_form = WizardFullForm(request.POST, prefix='growth')
        checklist_form = WizardPrerunChecklistForm(request.POST,
                                                   prefix='checklist')
        source_form = SourcesForm(request.POST, prefix='source')
        sample_formset = SampleFormSet(request.POST, prefix='sample')
        reservation_form = ReservationCloseForm(request.POST, prefix='reservation')

        if all([growth_form.is_valid(), source_form.is_valid(),
                checklist_form.is_valid(), sample_formset.is_valid(),
                reservation_form.is_valid()]):
            self.object = growth_form.save()
            source_form.save()
            for s in sample_formset:
                sample = s.save()
                sample.run_process(self.object)
            reservation_object = Reservation.get_latest(user=self.request.user,
                                                        tool_name='d180')
            if reservation_object is not None:
                if reservation_form.hold_open == False:
                    reservation_object.is_active = False
                    reservation_object.save()
            return HttpResponseRedirect(reverse('create_growth_d180_readings'))
        else:
            basic_info_form = WizardBasicInfoForm(request.POST, prefix='growth')
            growth_info_form = WizardGrowthInfoForm(request.POST, prefix='growth')
            comment_form = CommentsForm(request.POST, prefix='growth')
            return self.render_to_response(self.get_context_data(
                info_form=basic_info_form,
                growth_form=growth_info_form,
                checklist_form=checklist_form,
                source_form=source_form,
                comment_form=comment_form,
                sample_formset=sample_formset,
                reservation_form=reservation_form,
                reservation_object = Reservation().get_latest(user=self.request.user,
                                                              tool_name='d180')))


class WizardReadingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'growths/create_growth_readings.html'

    def get_object(self):
        return D180Growth.objects.latest('created')

    def build_forms(self, **kwargs):
        comment_form = CommentsForm(prefix='comment',
                                    initial={'comment': self.object.comment})
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
        context_data['samples'] = Sample.objects.get_by_process(
            self.object.uuid_full)
        return context_data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentsForm(request.POST, prefix='comment')
        readings = self.object.readings.get_queryset()
        readings_formset = D180ReadingsFormSet(request.POST, queryset=readings,
                                               prefix='reading')

        if comment_form.is_valid() and readings_formset.is_valid():
            self.object.comment = comment_form.cleaned_data['comment']
            self.object.save()
            for reading_form in readings_formset:
                if reading_form.has_changed():
                    reading_form.save(growth=self.object)
            return HttpResponseRedirect(reverse('create_growth_d180_readings'))
        else:
            return self.render_to_response(self.get_context_data(
                comment_form=comment_form,
                readings_formset=readings_formset,
            ))


class WizardPostrunView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'growths/create_growth_postrun.html'

    def get_object(self):
        return D180Growth.objects.latest('created')

    def build_forms(self):
        try:
            previous_source = D180Source.objects.latest('created')
        except ObjectDoesNotExist:
            previous_source = None

        return {
            'checklist_form': WizardPostrunChecklistForm(prefix='checklist'),
            'source_form': SourcesForm(instance=previous_source,
                                       prefix='source'),
            'comment_form': CommentsForm(prefix='growth'),
        }

    def get_context_data(self, **kwargs):
        context_data = super(WizardPostrunView, self).get_context_data(**kwargs)
        context_data['growth'] = self.object
        context_data['samples'] = Sample.objects.get_by_process(
            self.object.uuid_full)
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
            self.object.save()
            source_form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return self.render_to_response(self.get_context_data(
                checklist_form=checklist_form,
                source_form=source_form,
                comment_form=comment_form))
