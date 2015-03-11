# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import LoginRequiredMixin

from core.models import Process, Sample


class ProcessDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'core/process_detail.html'
    model = Process
    context_object_name = 'process'
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
        context = super(ProcessDetailView, self).get_context_data(**kwargs)
        context['samples'] = set(node.get_sample() for node in
                                 self.object.processnode_set.get_queryset())
        return context


class ProcessCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/process_create.html'
    model = Process
    fields = ('comment',)


class ProcessListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/process_list.html'
    model = Process


class ProcessUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'core/process_edit.html'
    model = Process
    context_object_name = 'process'
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


class RunProcessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/process_run.html'
