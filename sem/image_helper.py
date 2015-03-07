import os

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
                return allowed_sources[i]
        else:
            raise Exception('Unrecognizable')
    except Exception as e:
        raise Exception('Unable to process')

def _is_tiff(image):
    tmp = os.path.splitext(image)
    if tmp[1] == 'tif' or tmp[1] == 'tiff':
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
        return img.save(_process_name(image).join('.png'))

