# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import groupby
import logging

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import generic

import django_rq
from braces.views import LoginRequiredMixin

from core.forms import (DropzoneForm, ProcessCreateForm,
                        EditProcessTemplateForm, SampleFormSet,
                        WizardBasicInfoForm, ProcessTypeForm)
from core.models import Process, Sample, DataFile, ProcessTemplate, ProcessType, ProcessCategory
from core.tasks import process_file, save_files
from core.views import ActionReloadView


logger = logging.getLogger('emergence.process')


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
        nodes = self.object.nodes.order_by('number')
        context['sample_info'] = zip([n.get_sample() for n in nodes], nodes)
        context['datafiles'] = {k: list(g)
                                for k, g in groupby(self.object.datafiles.all(),
                                             lambda x: type(x))}
        return context


class ProcessListRedirectView(LoginRequiredMixin, generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('process_list', args=('all', self.request.user.username))


class ProcessListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/process_list.html'
    model = Process
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ProcessListView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username', 'all')

        process_categories = (ProcessCategory.objects
                                             .prefetch_related('processtypes')
                                             .order_by('slug'))

        if username != 'all':
            process_categories = process_categories.filter(
                processtype__process__user__username=username)
        process_categories = list(process_categories.annotate(number=Count('processtype__process')))
        excluded_categories = list(
            ProcessCategory.objects
                           .exclude(pk__in=[o.pk for o in process_categories]))

        for category in process_categories:
            if username == 'all':
                category.annotated = (category.processtypes.order_by('type')
                                                           .annotate(number=Count('process')))
            else:
                included_types = (category.processtypes.filter(process__user__username=username)
                                                           .order_by('type')
                                                           .annotate(number=Count('process')))
                excluded_types = (category.processtypes
                                          .exclude(pk__in=included_types.values_list('pk',
                                                                                     flat=True)
                                          .extra(select={'number': 0})))

                category.annotated = sorted(list(included_types) + list(excluded_types),
                                            key=lambda x: x.type)

        for category in excluded_categories:
            category.annotated = category.processtypes.order_by('type')

        process_categories.extend(excluded_categories)
        context['process_categories'] = process_categories
        context['active_users'] = get_user_model().active_objects.exclude(id=self.request.user.id)
        context['inactive_users'] = get_user_model().inactive_objects.order_by('-status_changed')
        context['slug'] = self.kwargs.get('slug', 'all')
        context['username'] = username
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug', 'all')
        username = self.kwargs.get('username', 'all')
        queryset = super(ProcessListView, self).get_queryset().order_by('-created')
        if username != 'all':
            queryset = queryset.filter(user__username=username)
        if slug != 'all':
            queryset = queryset.filter(type_id=slug)
        return queryset


class ProcessUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'core/process_edit.html'
    model = Process
    context_object_name = 'process'
    lookup_url_kwarg = 'uuid'
    fields = ('title', 'comment', )

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


class RunProcessView(LoginRequiredMixin, generic.CreateView):
    model = Process
    template_name = 'core/process_create.html'
    form_class = ProcessCreateForm
    process_type = 'generic-process'

    def get_initial(self):
        initial = super(RunProcessView, self).get_initial()
        initial['type'] = self.process_type
        return initial

    def get_form(self, form_class=ProcessCreateForm):
        try:
            sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        except Sample.DoesNotExist as e:
            raise Http404(e)
        return form_class(pieces=sample.pieces, user=self.request.user, **self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(RunProcessView, self).get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs['process_type'] = self.process_type
        return kwargs

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
        uuid = Process.strip_uuid(self.kwargs.get('uuid'))
        process = Process.objects.get(uuid_full__startswith=uuid)
        context['process'] = process
        nodes = process.nodes.order_by('number')
        context['sample_info'] = zip([n.get_sample() for n in nodes], nodes)
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
            queryset = queryset.filter(process__type_id=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcessTemplateListView, self).get_context_data(**kwargs)
        process_categories = list(
            (ProcessCategory.objects
                            .order_by('slug')
                            .prefetch_related('processtypes')
                            .annotate(number=Count('processtype__process__templates'))))

        for category in process_categories:
            category.annotated = (category.processtypes
                                          .order_by('type')
                                          .annotate(number=Count('process__templates')))

        context['process_categories'] = process_categories
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
                                                       title=process.title,
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
                user=self.request.user,
                prefix='process'),
            'sample_formset': SampleFormSet(prefix='sample'),
        }

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data(**self.build_forms()))

    def post(self, request, *args, **kwargs):
        self.object = None
        info_form = WizardBasicInfoForm(self.request.user, request.POST, prefix='process')
        sample_formset = SampleFormSet(request.POST, prefix='sample')

        if sample_formset.is_valid():
            logger.debug('Creating new process')
            self.object = info_form.save()
            logger.debug('Created process {} ({}) for {} samples'.format(
                self.object.uuid_full, self.object.legacy_identifier, len(sample_formset)))
            for n, s in enumerate(sample_formset):
                sample = s.save()
                logger.debug('Created sample {}'.format(sample.uuid))
                piece = s.cleaned_data['piece']
                sample.run_process(self.object, piece, n + 1)
            return HttpResponseRedirect(reverse('process_detail',
                                                kwargs={'uuid': self.object.uuid}))
        else:
            basic_info_form = WizardBasicInfoForm(self.request.user, request.POST,
                                                    prefix='process')
            return self.render_to_response(self.get_context_data(
                info_form=basic_info_form,
                sample_formset=sample_formset))


class TemplateProcessWizardView(ProcessWizardView):

    def build_forms(self):
        if 'id' in self.kwargs:
            template = ProcessTemplate.objects.get(id=self.kwargs.get('id', None))
            comment = template.comment
            process_type = template.process.type_id
        elif 'uuid' in self.kwargs:
            process = Process.objects.get(uuid_full__startswith=Process.strip_uuid(
                self.kwargs.get('uuid', None)))
            comment = process.comment
            process_type = process.type_id
        output = super(TemplateProcessWizardView, self).build_forms()
        output['info_form'] = WizardBasicInfoForm(self.request.user,
                                                  initial={'user': self.request.user,
                                                           'comment': comment,
                                                           'type': process_type},
                                                  prefix='process')
        return output


class ProcessTypeListView(LoginRequiredMixin, generic.ListView):
    model = ProcessType
    template_name = 'core/processtype_list.html'
    context_object_name = 'processtypes'

    def get_context_data(self, **kwargs):
        context = super(ProcessTypeListView, self).get_context_data(**kwargs)
        context['process_categories'] = (ProcessCategory.objects
                                                        .order_by('slug')
                                                        .prefetch_related('processtypes')
                                                        .annotate(number=Count('processtype')))
        return context


class ProcessTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = ProcessType
    template_name = 'core/processtype_detail.html'
    context_object_name = 'processtype'
    slug_field = 'type'

    def get_context_data(self, **kwargs):
        context = super(ProcessTypeDetailView, self).get_context_data(**kwargs)
        context['recent_processes'] = (Process.objects.filter(type_id=self.object.type)
                                                      .order_by('-created')[:10])
        return context


class ProcessTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ProcessType
    template_name = 'core/processtype_edit.html'
    context_object_name = 'processtype'
    slug_field = 'type'
    fields = ('name', 'full_name', 'description', 'category', 'scheduling_type',
              'creation_type')

    def get_success_url(self):
        return reverse('processtype_detail', args=(self.object.type,))


class ProcessTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProcessType
    template_name = 'core/processtype_create.html'
    form_class = ProcessTypeForm

    def get_success_url(self):
        return reverse('processtype_detail', args=(self.object.type,))


class ProcessCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProcessCategory
    template_name = 'core/processtype_create.html'
    fields = ('slug', 'name', 'description')

    def get_success_url(self):
        return reverse('processtype_list')
