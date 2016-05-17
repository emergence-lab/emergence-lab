# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.files.uploadedfile import InMemoryUploadedFile

import exifread
from PIL import Image
import six


allowed_sources = {
    'Image Tag 0x8546': 'leo1550',
    'Image Tag 0x877A': 'esem_600',
}


def get_image_source(image):
    try:
        image_obj = image.file
        tags = exifread.process_file(image)
        for i in allowed_sources.keys():
            if i in tags.keys():
                image_obj.seek(0)
                return allowed_sources[i]
        else:
            raise Exception('Unrecognizable')
    except Exception:
        raise Exception('Unable to process')


def _is_tiff(image):
    tmp = str(image).split('.')[1]
    return str(tmp) in ['tif', 'tiff']


def _process_name(image):
    return str(image).split('.')[0]


def get_sample(image):
    return _process_name(image).split('_')[0].split('s')[1]


def get_image_number(image):
    text = _process_name(image)
    return text.split('_')[1]


def convert_tiff(image):
    if not _is_tiff(image):
        return image

    img = Image.open(image)
    tempio = six.BytesIO()
    img.save(tempio, format='PNG')
    return InMemoryUploadedFile(
        tempio, field_name=None, name=(_process_name(image) + '.png'),
        content_type='image/png', size=len(tempio.getvalue()), charset=None)
