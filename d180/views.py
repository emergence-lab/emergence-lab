# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import LoginRequiredMixin

from .models import D180Source, Platter
from .forms import (CommentsForm, SourcesForm, WizardBasicInfoForm,
                    WizardGrowthInfoForm, WizardFullForm,
                    WizardPrerunChecklistForm)
from core.views import ActionReloadView, ActiveListView
from core.forms import SampleFormSet


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

        return {
            'info_form': WizardBasicInfoForm(initial={'user': self.request.user},
                                             prefix='growth'),
            'growth_form': WizardGrowthInfoForm(prefix='growth'),
            'checklist_form': WizardPrerunChecklistForm(prefix='checklist'),
            'source_form': SourcesForm(instance=previous_source,
                                       prefix='source'),
            'comment_form': CommentsForm(prefix='growth'),
            'sample_formset': SampleFormSet(prefix='sample'),
        }

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(
            self.get_context_data(**self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = None
        growth_form = WizardFullForm(request.POST, prefix='growth')
        checklist_form = WizardPrerunChecklistForm(request.POST,
                                                   prefix='checklist')
        source_form = SourcesForm(request.POST, prefix='source')
        sample_formset = SampleFormSet(request.POST, prefix='sample')

        if growth_form.is_valid() and source_form.is_valid() and checklist_form.is_valid() and sample_formset.is_valid():
            self.object = growth_form.save()
            print('growth uuid: {}'.format(self.object.uuid))
            source_form.save()
            for s in sample_formset:
                sample = s.save()
                print('sample uuid: {}'.format(sample.uuid))
                sample.run_process(self.object)
            return HttpResponseRedirect(reverse('create_growth_d180_start'))
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
                sample_formset=sample_formset))
