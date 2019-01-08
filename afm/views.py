# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse

from afm.models import AFMFile
from afm.tasks import process_nanoscope_file
from core.views import RunProcessView, UploadFileView


class AFMFileUpload(UploadFileView):
    """
    Add files to an existing afm process
    """
    model = AFMFile
    rq_config = {
        'process': process_nanoscope_file,
    }


class AutocreateAFMView(RunProcessView):
    """
    View for creation of new afm data.
    """
    process_type = 'afm'

    def get_success_url(self):
        return reverse('afm_upload', args=(self.object.uuid,))
