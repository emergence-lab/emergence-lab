# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings

from collections import namedtuple
import logging
import os

import django_rq


logger = logging.getLogger(__name__)


AsyncDjangoFile = namedtuple('AsyncDjangoFile', ['data', 'kwargs'])


@django_rq.job
def process_file(raw_file):
    return [AsyncDjangoFile(raw_file, {})]


@django_rq.job
def save_files(model, process, job_id, queue='default'):
    queue = django_rq.get_queue(queue)
    logger.debug('Retrieving results for job {} from queue {}'.format(
        job_id, queue.name))
    processed_files = queue.fetch_job(job_id).result

    for f, kwargs in processed_files:
        logger.debug('Saving file \'{}\' for process {}'.format(
            f.name, process.uuid_full))

        if 'content_type' not in kwargs:
            try:
                kwargs['content_type'] = f.content_type
            except AttributeError:
                kwargs['content_type'] = 'application/octet-stream'

        obj = model.objects.create(
            data=None, process=process, **kwargs)
        obj.data = f
        obj.save()
        try:
            f.close_and_delete()
        except AttributeError:
            pass
        _save_sample_files(process, obj)


def _save_sample_files(process, file_object):
    """
    Create hard links in sample-specific folders to the datafile in the
    process-specific folder.

    Create sample-specific directory structure:
      samples/<sample.uuid>/<process.type_id>/<process.uuid_full.hex>/
    and create a hard link to the file in the process-specific
    directory structure:
      processes/<process.uuid_full.hex>/
    """
    for sample in process.samples:
        sample_dir = os.path.abspath(os.path.join(
            settings.MEDIA_ROOT, 'samples', sample.uuid, process.type_id))
        target_dir = os.path.join(sample_dir, process.uuid_full.hex)
        try:
            os.makedirs(target_dir)
            logger.debug('created directory {}'.format(target_dir))
        except OSError:
            pass
        source_dir, filename = os.path.split(os.path.abspath(file_object.data.path))
        target = os.path.join(target_dir, filename)
        source = os.path.join(source_dir, filename)
        logger.debug('linking {} to {}'.format(target, source))
        os.link(source, target)
