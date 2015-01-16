# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from .filters import growth_filter
from .models import D180Growth, D180Readings
from .serializers import D180GrowthSerializer, D180ReadingsSerializer


class D180GrowthListAPI(generics.ListCreateAPIView):
    """
    List all growths or create a new one via api.
    """
    queryset = D180Growth.objects.all()
    serializer_class = D180GrowthSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = growth_filter


class D180GrowthDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update a growth.
    """
    queryset = D180Growth.objects.all()
    serializer_class = D180GrowthSerializer
    permission_classes = (permissions.IsAuthenticated,)


class D180ReadingsListAPI(generics.ListCreateAPIView):
    """
    List all readings or create a new one via api.
    """
    queryset = D180Readings.objects.all()
    serializer_class = D180ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class D180ReadingsCreateAPI(generics.CreateAPIView):
    """
    Create a new reading via api.
    """
    serializer_class = D180ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class D180ReadingsDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update readings.
    """
    queryset = D180Readings.objects.all()
    serializer_class = D180ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated,)
