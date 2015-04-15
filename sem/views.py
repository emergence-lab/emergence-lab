# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView,
                                  UpdateView, )

from braces.views import LoginRequiredMixin

from core.forms import DropzoneForm
from core.models import DataFile, SampleManager, Process
from core.views import ActionReloadView, CreateUploadProcessView
from sem.forms import AutoCreateSEMForm
from sem.models import SEMScan
from sem.image_helper import convert_tiff


class AutocreateSEMView(CreateUploadProcessView):
    """
    Creates an sem process to for SEMAddFiles view
    """
    model = SEMScan
    form_class = AutoCreateSEMForm

    def get_success_url(self):
        return reverse('sem_upload', args=(self.object.uuid,))


class SEMFileUpload(LoginRequiredMixin, CreateView):
    """
    Add files to an existing sem process
    """
    model = DataFile
    template_name = 'core/process_upload.html'
    form_class = DropzoneForm

    def get_context_data(self, **kwargs):
        context = super(SEMFileUpload, self).get_context_data(**kwargs)
        context['process'] = self.kwargs['uuid']
        return context

    def form_valid(self, form):
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))

        image = self.request.FILES['file']
        image = convert_tiff(image)

        with transaction.atomic():
            obj = DataFile.objects.create(data=image,
                                          content_type=image.content_type)
            obj.processes.add(process)

        return JsonResponse({'status': 'success'})
