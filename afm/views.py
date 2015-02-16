# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .models import AFMScan


class AFMList(LoginRequiredMixin, ListView):
    """
    List the most recent afm data
    """
    model = AFMScan
    template_name = 'afm/afm_list.html'
    paginate_by = 25


class AFMDetail(LoginRequiredMixin, DetailView):
    """
    Detail view of the afm model.
    """
    model = AFMScan
    template_name = 'afm/afm_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AFMDetail, self).get_context_data(**kwargs)
        context['sample_siblings'] = []
        context['pocket_siblings'] = []
        context['growth_siblings'] = []
        return context


class AFMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_create.html'


class AFMUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_update.html'


class AFMDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting afm data
    """
    model = AFMScan
    template_name = 'afm/afm_delete.html'

    def get_success_url(self):
        return reverse('afm_list')
