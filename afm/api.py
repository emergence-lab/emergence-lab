# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from .models import AFMScan
from .serializers import AFMSerializer


class AFMListCreateAPIView(generics.ListCreateAPIView):
    """
    List all afm scans or create a new one via api.
    """
    queryset = AFMScan.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AFMRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Show details or update an afm scan.
    """
    queryset = AFMScan.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated,)
