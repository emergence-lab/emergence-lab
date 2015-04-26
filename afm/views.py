# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from afm.forms import AutoCreateAFMForm
from afm.models import AFMFile, AFMScan
from afm.tasks import process_nanoscope_file
from core.views import CreateUploadProcessView, UploadFileView


class AFMFileUpload(UploadFileView):
    """
    Add files to an existing afm process
    """
    model = AFMFile
    rq_config = {
        'process': process_nanoscope_file,
    }


class AutocreateAFMView(CreateUploadProcessView):
    """
    View for creation of new afm data.
    """
    model = AFMScan
    form_class = AutoCreateAFMForm

    def get_success_url(self):
        return reverse('afm_upload', args=(self.object.uuid,))
