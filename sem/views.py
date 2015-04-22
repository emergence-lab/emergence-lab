# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from core.views import CreateUploadProcessView, UploadFileView
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


class SEMFileUpload(UploadFileView):
    """
    Add files to an existing sem process
    """

    def process_file(self, uploaded_file):
        return [(convert_tiff(uploaded_file), {})]