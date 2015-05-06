# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import groupby
import logging

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic

import django_rq
from braces.views import LoginRequiredMixin

from core.forms import (DropzoneForm, ProcessCreateForm,
                        EditProcessTemplateForm, SampleFormSet,
                        WizardBasicInfoForm)
from core.models import Process, Sample, DataFile, ProcessTemplate
from core.polymorphic import get_subclasses
from core.tasks import process_file, save_files
from core.views import ActionReloadView


logger = logging.getLogger(__name__)


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
    fields = ('comment', 'user',)

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class ProcessListRedirectView(LoginRequiredMixin, generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('process_list', args=('all', 'all'))


class ProcessListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/process_list.html'
    model = Process
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ProcessListView, self).get_context_data(**kwargs)
        context['process_list'] = get_subclasses(Process)
        context['user_list'] = get_user_model().objects.all().filter(is_active=True)
        context['slug'] = self.kwargs.get('slug', 'all')
        context['username'] = self.kwargs.get('username', 'all')
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug', 'all')
        username = self.kwargs.get('username', 'all')
        queryset = super(ProcessListView, self).get_queryset().order_by('-created')
        if username != 'all':
            queryset = queryset.filter(user__username=username)
        if slug != 'all':
            queryset = [i for i in queryset if i.slug == slug]
        return queryset


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

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class CreateUploadProcessView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/process_create.html'

    def get_form(self, form_class):
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        return form_class(pieces=sample.pieces, **self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        pieces = form.cleaned_data['pieces']
        sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        for piece in pieces:
            sample.run_process(self.object, piece=piece)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('process_detail', args=(self.object.uuid,))


class RunProcessView(CreateUploadProcessView):
    model = Process
    form_class = ProcessCreateForm


class UploadFileView(LoginRequiredMixin, generic.CreateView):
    """
    Add files to an existing process
    """
    model = DataFile
    template_name = 'core/process_upload.html'
    form_class = DropzoneForm
    rq_config = {
        'process': process_file,
        'save': save_files,
    }
    rq_queue = 'default'

    def get_context_data(self, **kwargs):
        context = super(UploadFileView, self).get_context_data(**kwargs)
        context['process'] = self.kwargs['uuid']
        return context

    def form_valid(self, form):
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))

        uploaded_file = self.request.FILES['file']
        logger.debug('Uploaded file \'{}\' for process {}'.format(
            uploaded_file.name, process.uuid_full))

        queue = django_rq.get_queue(self.rq_queue)
        result = queue.enqueue(self.rq_config.get('process', process_file), uploaded_file)
        queue.enqueue_call(
            func=self.rq_config.get('save', save_files),
            args=(self.model, process, result.id, self.rq_queue,),
            depends_on=result)

        return JsonResponse({'status': 'success'})


class ProcessTemplateListView(LoginRequiredMixin, generic.ListView):
    """
    View for favorite process comment templates.
    """
    model = ProcessTemplate
    template_name = 'core/process_templates.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug', 'all')
        queryset = super(ProcessTemplateListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-created')
        if slug != 'all':
            queryset = [i for i in queryset if i.process.slug == slug]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcessTemplateListView, self).get_context_data(**kwargs)
        context['process_list'] = get_subclasses(Process)
        context['slug'] = self.kwargs.get('slug', 'all')
        return context


class AddProcessTemplateView(LoginRequiredMixin, ActionReloadView):
    """
    View for adding a process template
    """

    def perform_action(self, request, *args, **kwargs):
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs.get('uuid', None)))
        self.template = ProcessTemplate.objects.create(process=process,
                                                       comment=process.comment,
                                                       user=self.request.user,
                                                       name=process.uuid)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('process_template_detail', kwargs={'pk': self.template.id})


class RemoveProcessTemplateView(LoginRequiredMixin, generic.DeleteView):
    """
    View for deleting a process template
    """
    model = ProcessTemplate

    def get_success_url(self, *args, **kwargs):
        return reverse('process_templates', kwargs={'slug': 'all'})


class ProcessTemplateDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View for process template details
    """
    model = ProcessTemplate
    template_name = 'core/process_template_detail.html'


class ProcessTemplateEditView(LoginRequiredMixin, generic.UpdateView):
    """
    View for editing process template details
    """
    model = ProcessTemplate
    template_name = 'core/process_template_edit.html'
    form_class = EditProcessTemplateForm

    def get_success_url(self):
        return reverse('process_template_detail', args=(self.object.id,))


class ProcessWizardView(LoginRequiredMixin, generic.TemplateView):
    """
    Steps through creating a process.
    """
    template_name = 'core/process_wizard_create.html'

    def build_forms(self):
        return {
            'info_form': WizardBasicInfoForm(
                initial={
                    'user': self.request.user,
                },
                prefix='process'),
            'sample_formset': SampleFormSet(prefix='sample'),
        }

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data(**self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = None
        info_form = WizardBasicInfoForm(request.POST, prefix='process')
        sample_formset = SampleFormSet(request.POST, prefix='sample')

        if sample_formset.is_valid():
            logger.debug('Creating new process')
            self.object = info_form.save()
            logger.debug('Created process {} ({}) for {} samples'.format(
                self.object.uuid_full, self.object.legacy_identifier, len(sample_formset)))
            for s in sample_formset:
                sample = s.save()
                logger.debug('Created sample {}'.format(sample.uuid))
                piece = s.cleaned_data['piece']
                sample.run_process(self.object, piece)
            return HttpResponseRedirect(reverse('process_detail',
                                                kwargs={'uuid': self.object.uuid}))
        else:
            basic_info_form = WizardBasicInfoForm(request.POST, prefix='process')
            return self.render_to_response(self.get_context_data(
                info_form=basic_info_form,
                sample_formset=sample_formset))


class TemplateProcessWizardView(ProcessWizardView):

    def build_forms(self):
        if 'id' in self.kwargs:
            comment = ProcessTemplate.objects.get(id=self.kwargs.get('id', None)).comment
        elif 'uuid' in self.kwargs:
            comment = Process.objects.get(uuid_full__startswith=Process.strip_uuid(
                self.kwargs.get('uuid', None))).comment
        output = super(TemplateProcessWizardView, self).build_forms()
        output['info_form'] = WizardBasicInfoForm(initial={'user': self.request.user,
                                                           'comment': comment}, prefix='process')
        return output
