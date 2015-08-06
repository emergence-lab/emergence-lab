# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from core.views import RunProcessView, UploadFileView
from sem.tasks import process_sem_file


class AutocreateSEMView(RunProcessView):
    """
    Creates an sem process to for SEMAddFiles view
    """
    process_type = 'sem'

    def get_success_url(self):
        return reverse('sem_upload', args=(self.object.uuid,))


class SEMFileUpload(UploadFileView):
    """
    Add files to an existing sem process
    """
    rq_config = {
        'process': process_sem_file,
    }
