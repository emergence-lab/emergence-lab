# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.core.files.uploadedfile import InMemoryUploadedFile

import django_rq
import nanoscope
from PIL import Image, ImageDraw, ImageFont
import six

from core.tasks import AsyncDjangoFile


logger = logging.getLogger(__name__)


@django_rq.job
def process_nanoscope_file(raw_file):
    scan_number = int(os.path.splitext(raw_file.name)[-1][1:])
    if '_' in raw_file.name:
        location = os.path.splitext(raw_file.name)[0].split('_')[-1]
        if location not in 'rRcCfFeE':
            location = 'c'
    else:
        location = 'c'
    logger.debug(
        'Extracted scan_number={}, location={}'.format(scan_number, location))
    raw = six.BytesIO(raw_file.read())
    raw.mode = 'b'
    scan = nanoscope.read(raw, encoding='cp1252')
    logger.debug('Read in file {}'.format(raw_file.name))

    processed_files = [
        AsyncDjangoFile(raw_file,
                        dict(image_type='Raw', state='raw',
                             rms=0.0, zrange=0.0,
                             size=0.0, scan_number=scan_number,
                             content_type='application/octet-stream'))]
    for img in scan:
        processed_image = _create_scan_png(img, raw_file.name, scan_number)
        logger.debug('Created image file for {} scan'.format(img.type))
        scan_size = math.sqrt(img.scan_area)
        processed_files.append(
            AsyncDjangoFile(processed_image,
                            dict(image_type=img.type, state='extracted',
                                 rms=img.rms, zrange=img.zrange,
                                 size=scan_size, scan_number=scan_number)))
    processed_files[0].size = scan_size
    return processed_files


def _create_scan_png(scan, filename, scan_number):
    """
    Create standard png with afm and summary information.
    """
    image = Image.fromarray(scan.colorize())
    if image.size != (512, 512):
        logger.debug('Image not correct size: {}, should be 512 x 512'.format(image.size))
        image = image.resize((512, 512), resample=Image.NEAREST)
        logger.debug('Resized image to 512 x 512')

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
