# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from afm.models import AFMFile, AFMScan
from core.models import Process


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
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_context_data(self, **kwargs):
        context = super(AFMDetail, self).get_context_data(**kwargs)
        context['sample_siblings'] = []
        context['pocket_siblings'] = []
        context['growth_siblings'] = []
        context['dataset'] = self.object.datafiles.get_queryset().instance_of(AFMFile)
        return context


class AFMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_create.html'

    def get_success_url(self):
        return reverse('afm_detail', args=(self.object.uuid,))


class AFMUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_update.html'
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'
    fields = ('comment',)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('afm_detail', args=(self.object.uuid,))


class AFMDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting afm data
    """
    model = AFMScan
    template_name = 'afm/afm_delete.html'
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('afm_list')
