# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.core.urlresolvers import reverse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView,
                                  UpdateView, RedirectView,)
from braces.views import LoginRequiredMixin

from core.models import Sample, DataFile
from core.views import ActionReloadView
from .models import SEMScan
from .forms import DropzoneForm
from .response import JSONResponse, response_mimetype
from .image_helper import (get_image_source, get_sample,
                           convert_tiff,)


class SEMList(LoginRequiredMixin, ListView):
    """
    List the most recent sem data
    """
    model = SEMScan
    template_name = 'sem/sem_list.html'
    paginate_by = 25


class SEMAutoCreate(LoginRequiredMixin, ActionReloadView):
    """
    Creates an sem process to for SEMAddFiles view
    """
    def perform_action(self, request, *args, **kwargs):
        process = SEMScan.objects.create()
        sample = sample.objects.get(id=self.kwargs['sample'])
        sample.run_process(process)
        self.process_id = process.id

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sem_files', args=(self.process_id,))


class SEMAddFiles(LoginRequiredMixin, CreateView):
    """
    Add files to an existing sem process
    """
    model = DataFile
    template_name = 'sem/sem_upload.html'
    form_class = DropzoneForm

    def form_valid(self, form):
        image = self.request.FILES['file']
        source = get_image_source(image)
        image = convert_tiff(image)
        process = SEMScan.objects.get(id=self.kwargs['process'])
        with transaction.atomic():
            obj = DataFile.objects.create(image=image,
                                          content_type='image')
            obj.processes.add(process)
        data = {'status': 'success'}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        return response


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


#class SEMUpload(LoginRequiredMixin, CreateView):
#    """
#    View for creation of new sem data.
#    """
#    model = SEMScan
#    template_name = 'sem/sem_upload.html'
#    form_class = DropzoneForm
#
#    def form_valid(self, form):
#        image = self.request.FILES['file']
#        source = get_image_source(image)
#        try:
#            sample = get_sample(image)
#        except:
#            sample = None
#        image = convert_tiff(image)
#        with transaction.atomic():
#            obj = SEMScan.objects.create(image_source=source,
#                                         image_number=0,
#                                         image=image)
#            if sample:
#                s = Sample.objects.get(id=sample)
#                s.run_process(obj)
#        data = {'status': 'success'}
#        response = JSONResponse(data, mimetype=response_mimetype(self.request))
#        return response


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
