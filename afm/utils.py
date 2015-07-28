# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import re


def extract_scan_number(filename):
    """
    Extracts the scan number from the filename extension, which should be a
    zero-padded number.
    """
    return int(os.path.splitext(filename)[-1].replace('.', ''))


def extract_scan_location(filename, default_location='c'):
    """
    Extracts the scan location from the filename. Filename should be in the
    format:
        file_c.ext
    Where 'c' will be the extracted location and '-' or '_' can be used as the
    separating character.
    """
    if re.search(r'[\-_]', filename) is None:
        return default_location

    location = re.split(r'[\-_]', os.path.splitext(filename)[0])[-1]

    if len(location) != 1 or location not in 'rRcCfFeE':
        return default_location

    return location
