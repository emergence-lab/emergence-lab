# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from .models import SEMScan
from .serializers import SEMSerializer


class SEMListCreateAPIView(generics.ListCreateAPIView):
    """
    List all sem scans or create a new one via api.
    """
    queryset = SEMScan.objects.all()
    serializer_class = SEMSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SEMRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Show details or update an sem scan.
    """
    queryset = SEMScan.objects.all()
    serializer_class = SEMSerializer
    permission_classes = (permissions.IsAuthenticated,)
