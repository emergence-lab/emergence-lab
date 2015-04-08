# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import groupby

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.contenttypes.models import ContentType

from braces.views import LoginRequiredMixin

from core.models import Process, Sample, DataFile, SplitProcess
from core.forms import DropzoneForm


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
        context['datafiles'] = {k: list(g)
                                for k, g in groupby(self.object.datafiles.all(),
                                             lambda x: type(x))}
        if type(self.object).name == 'D180 Growth':
            context['readings'] = True
        return context


class ProcessCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/process_create.html'
    model = Process
    fields = ('comment',)

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class ProcessListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/process_list.html'
    model = Process

    def get_queryset(self):
        queryset = super(ProcessListView, self).get_queryset()
        return queryset.order_by('-created')


class ProcessUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'core/process_edit.html'
    model = Process
    context_object_name = 'process'
    lookup_url_kwarg = 'uuid'
    fields = ('-comment',)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class RunProcessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/process_run.html'


class CreateUploadProcessView(LoginRequiredMixin, generic.CreateView):

    def get_form(self, form_class):
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        return form_class(pieces=sample.pieces, **self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save()
        pieces = form.cleaned_data['pieces']
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        for piece in pieces:
            sample.run_process(self.object, piece=piece)
        return HttpResponseRedirect(self.get_success_url())


class UploadFileView(LoginRequiredMixin, generic.CreateView):
    """
    Add files to an existing sem process
    """
    model = DataFile
    template_name = 'core/file_upload.html'
    form_class = DropzoneForm

    def get_context_data(self, **kwargs):
        context = super(UploadFileView, self).get_context_data(**kwargs)
        context['process'] = self.kwargs['uuid']
        return context

    def form_valid(self, form):
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))

        image = self.request.FILES['file']

        with transaction.atomic():
            obj = DataFile.objects.create(data=image,
                                          content_type=image.content_type)
            obj.processes.add(process)

        return JsonResponse({'status': 'success'})
