# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings

from rest_framework.views import APIView
from rest_framework import permissions
from sendfile import sendfile


class FileAccessAPI(APIView):
    """
    REST equivalent of core/views/utility/ProtectedMediaView
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, filename):
        """
        Uses sendfile to get requested file and returns file object
        """

        return sendfile(request, os.path.join(settings.MEDIA_ROOT, filename))
