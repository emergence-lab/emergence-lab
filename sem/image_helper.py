import os
from io import BytesIO
import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
import exifread


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
    except Exception as e:
        raise Exception('Unable to process')

def _is_tiff(image):
    tmp = str(image).split('.')[1]
    if str(tmp) == 'tif' or str(tmp) == 'tiff':
        return True
    else:
        return False

def _process_name(image):
    return str(image).split('.')[0]

def get_sample(image):
    return _process_name(image).split('_')[0].split('s')[1]

def get_image_number(image):
    text = _process_name(image)
    return text.split('_')[1]

def convert_tiff(image):
    if _is_tiff(image):
        img = Image.open(image)
        tmp = open(tempfile.NamedTemporaryFile().name, 'wb+')
        tmp.seek(0)
        final = img.save(tmp, format='png')
        output = InMemoryUploadedFile(file=tmp,
                                      field_name=None,
                                      name=str(_process_name(image) + '.png'),
                                      content_type='image/png',
                                      size=tmp.tell(),
                                      charset=None)
        return output
    else:
        return image

