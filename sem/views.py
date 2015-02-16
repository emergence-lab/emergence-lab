# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .models import SEMScan


class SEMList(LoginRequiredMixin, ListView):
    """
    List the most recent sem data
    """
    model = SEMScan
    template_name = 'sem/sem_list.html'
    paginate_by = 25


class SEMDetail(LoginRequiredMixin, DetailView):
    """
    Detail view of the sem model.
    """
    model = SEMScan
    template_name = 'sem/sem_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SEMDetail, self).get_context_data(**kwargs)
        context['sample_siblings'] = []
        context['pocket_siblings'] = []
        context['growth_siblings'] = []
        return context


class SEMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_create.html'


class SEMUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating sem data.
    """
    model = SEMScan
    template_name = 'sem/sem_update.html'


class SEMDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting sem data
    """
    model = SEMScan
    template_name = 'sem/sem_delete.html'

    def get_success_url(self):
        return reverse('sem_list')
