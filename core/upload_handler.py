# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import errno
import io
import logging
import os

from django.conf import settings
from tempfile import NamedTemporaryFile
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import UploadedFile


logger = logging.getLogger(__name__)


class RQTemporaryUploadedFile(UploadedFile):

    def __init__(self, name, content_type, size, charset,
                 content_type_extra=None, existing_path=None):
        if existing_path is not None:
            logger.debug('opening existing file: {}'.format(existing_path))
            f = io.open(existing_path, 'r+b')
            f.read()
        else:
            f = NamedTemporaryFile(suffix='.upload', delete=False,
                                   dir=settings.FILE_UPLOAD_TEMP_DIR)
            logger.debug('created new file: {}'.format(f.name))
        super(RQTemporaryUploadedFile, self).__init__(
            f, name, content_type, size, charset, content_type_extra)

    def temporary_file_path(self):
        return self.file.name

    def close(self):
        try:
            return self.file.close()
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def close_and_delete(self):
        self.close()
        os.unlink(self.temporary_file_path())

    def __reduce__(self):
        self.close()
        return (
            self.__class__,
            (self.name, self.content_type, self.size, self.charset,
             self.content_type_extra, self.temporary_file_path()),)


class RQTemporaryFileUploadHandler(FileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(RQTemporaryFileUploadHandler, self).__init__(*args, **kwargs)

    def new_file(self, *args, **kwargs):
        super(RQTemporaryFileUploadHandler, self).new_file(*args, **kwargs)
        self.file = RQTemporaryUploadedFile(
            self.file_name, self.content_type, 0, self.charset, self.content_type_extra)

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file
