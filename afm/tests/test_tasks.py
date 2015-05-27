# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.forms import ValidationError
from django.test import TestCase

from django_rq import get_queue
from rq import SimpleWorker

from afm import tasks
from afm.models import AFMFile


class TestProcessFiles(TestCase):

    def test_process_header_only(self):
        """
        Test that the task will properly process the file and extract
        location and scan_number from the filename, with the rest of the
        values being default.
        """
        file_data = ('\\*File list\n'
                     '\\Version: 0x05120130\n'
                     '\\*File list end\n')

        scan_file = SimpleUploadedFile('s0001a_r.001',
                                       file_data.encode('cp1252'),
                                       content_type='text/plain')

        queue = get_queue('default', async=False)
        job = queue.enqueue(tasks.process_nanoscope_file, scan_file)

        self.assertEqual(len(job.result), 1)

        data = {
            'rms': 0.0,
            'zrange': 0.0,
            'size': 0.0,
            'scan_number': 1,
            'location': 'r',
            'image_type': 'Raw',
            'state': 'raw',
            'content_type': 'application/octet-stream',
        }
        self.assertDictEqual(job.result[0].kwargs, data)

    def test_process_image_data(self):
        file_data = ('\\*File list\n'
                     '\\Version: 0x05120130\n'
                     '\\@Sens. Zscan: V 9 nm/V\n'
                     '\\*Ciao image list\n'
                     '\\Data offset: 368\n'
                     '\\Data length: 12\n'
                     '\\Bytes/pixel: 1\n'
                     '\\Number of lines: 2\n'
                     '\\Samps/line: 6\n'
                     '\\Scan size: 1 1 ~m\n'
                     '\\@2:Image Data: S [Amplitude] "Amplitude"\n'
                     '\\@Z magnify: C [2:Z scale] 1\n'
                     '\\@2:Z scale: V [Sens. Amplitude] (1 V/LSB) 1 V\n'
                     '\\@2:Z offset: V [Sens. Amplitude] (1 V/LSB) 1 V\n'
                     '\\*File list end\n'
                     '......'
                     '\n 2\n 2'
                     '\n 2\n 2\n')
        scan_file = SimpleUploadedFile('s0001a_r.001',
                                       file_data.encode('cp1252'),
                                       content_type='text/plain')

        queue = get_queue('default', async=False)
        job = queue.enqueue(tasks.process_nanoscope_file, scan_file)

        self.assertEqual(len(job.result), 2)  # raw & extracted file

        data = {
            'rms': 0.50905796786656576,
            'zrange': 1.58203125,
            'size': 1.0,
            'scan_number': 1,
            'location': 'r',
            'image_type': 'Amplitude',
            'state': 'extracted',
            'content_type': 'image/png',
        }
        self.assertDictEqual(job.result[-1].kwargs, data)

    def test_process_wrong_filetype(self):
        file_data = 'plain text data'
        scan_file = SimpleUploadedFile('s0001a_r.001',
                                       file_data.encode('cp1252'),
                                       content_type='text/plain')

        queue = get_queue('default', async=False)
        with self.assertRaises(ValueError):
            queue.enqueue(tasks.process_nanoscope_file, scan_file)
