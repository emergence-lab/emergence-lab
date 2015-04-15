# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import math
import os

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse

import nanoscope
from PIL import Image, ImageDraw, ImageFont
import six

from afm.models import AFMFile, AFMScan
from afm.forms import AutoCreateAFMForm
from core.views import CreateUploadProcessView, UploadFileView


class AFMFileUpload(UploadFileView):
    """
    Add files to an existing afm process
    """
    model = AFMFile

    def process_image(self, scan, filename, scan_number):
        image = Image.fromarray(scan.colorize())

        processed_image = Image.new(image.mode, (654, 580), 'white')
        processed_image.paste(image,
                              (20, 20, image.size[0] + 20, image.size[1] + 20))

        calibri = ImageFont.truetype(
            os.path.join(settings.STATIC_ROOT, 'afm', 'fonts', 'calibrib.ttf'),
            20)
        draw = ImageDraw.Draw(processed_image)

        scale_image = Image.open(
            os.path.join(settings.STATIC_ROOT, 'afm', 'img', 'scale_12.png'))
        processed_image.paste(scale_image,
                             (28 + image.size[0],
                              30,
                              28 + image.size[0] + scale_image.size[0],
                              30 + scale_image.size[1]))
        if scan.type == 'Height':
            unit = 'nm'
        else:
            unit = 'V'
        draw.text(
            (28 + image.size[0] + scale_image.size[0] + 7, 25),
            '{0:.0f} {1}'.format(scan.height_scale, unit), 'black', calibri)
        draw.text(
            (28 + image.size[0] + scale_image.size[0] + 7, 20 + scale_image.size[1]),
            '0.0 {}'.format(unit), 'black', calibri)

        zrange_str = 'Z-Range: {0:.2f} nm'.format(scan.zrange)
        rms_str = 'RMS: {0:.2f} nm'.format(scan.rms)
        size_str = 'Area: {0} \u03bcm X {0} \u03bcm'.format(math.sqrt(scan.scan_area))

        draw.text((20, 25 + image.size[1]), filename, 'black', calibri)
        draw.text(
            (20 + image.size[0] - calibri.getsize(size_str)[0], 25 + image.size[1]),
            size_str, 'black', calibri)
        if scan.type == 'Height':
            draw.text(
                (20, 50 + image.size[1]), zrange_str, 'black', calibri)
            draw.text(
                (20 + image.size[0] - calibri.getsize(rms_str)[0], 50 + image.size[1]),
                rms_str, 'black', calibri)
        else:
            type_str = '{} AFM'.format(scan.type)
            draw.text(
                (20 + image.size[0] - calibri.getsize(type_str)[0], 50 + image.size[1]),
                type_str, 'black', calibri)

        tempio = six.StringIO()
        processed_image.save(tempio, format='PNG')
        return InMemoryUploadedFile(
            tempio, field_name=None, name=filename + '.png',
            content_type='image/png', size=tempio.len, charset=None)

    def process_file(self, process, uploaded_file):
        scan_number = int(os.path.splitext(uploaded_file.name)[-1][1:])
        raw = six.BytesIO(uploaded_file.read())
        raw.mode = 'b'
        scan = nanoscope.read(raw, encoding='cp1252')
        return (scan, {'scan_number': scan_number})

    def save_file(self, process, processed_file, raw_file, content_type=None, **file_kwargs):
        scan_number = file_kwargs.get('scan_number', 0)
        obj = self.model.objects.create(data=raw_file,
                                        content_type='application/octet-stream',
                                        image_type='Raw',
                                        state='raw',
                                        rms=0.0,
                                        zrange=0.0,
                                        size=0.0,
                                        scan_number=scan_number)
        obj.processes.add(process)

        for img in processed_file:
            img.process()
            processed_image = self.process_image(img, raw_file.name, scan_number)
            img_file = self.model.objects.create(
                data=processed_image,
                content_type=processed_image.content_type,
                state='extracted',
                rms=img.rms,
                zrange=img.zrange,
                size=img.scan_area,
                image_type=img.type,
                scan_number=scan_number)
            img_file.processes.add(process)


class AutocreateAFMView(CreateUploadProcessView):
    """
    View for creation of new afm data.
    """
    model = AFMScan
    form_class = AutoCreateAFMForm

    def get_success_url(self):
        return reverse('afm_upload', args=(self.object.uuid,))
