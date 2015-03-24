# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from .models import Hall
from .serializers import HallSerializer


class HallListCreateAPIView(generics.ListCreateAPIView):
    """
    List all hall scans or create a new one via api.
    """
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HallRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Show details or update an hall scan.
    """
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (permissions.IsAuthenticated,)
