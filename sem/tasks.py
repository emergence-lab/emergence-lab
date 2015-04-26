# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django_rq

from core.tasks import AsyncDjangoFile
from sem.image_helper import convert_tiff


@django_rq.job
def process_sem_file(raw_file):
    return [AsyncDjangoFile(convert_tiff(raw_file), {})]
