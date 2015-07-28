# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from core.models import Process
from d180.models import D180Readings
from .serializers import D180GrowthSerializer, D180ReadingsSerializer


class D180GrowthListAPI(generics.ListCreateAPIView):
    """
    List all growths or create a new one via api.
    """
    queryset = Process.objects.filter(type_id='d180-growth')
    serializer_class = D180GrowthSerializer
    permission_classes = (permissions.IsAuthenticated,)


class D180GrowthDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update a growth.
    """
    queryset = Process.objects.filter(type_id='d180-growth')
    serializer_class = D180GrowthSerializer
    permission_classes = (permissions.IsAuthenticated,)


class D180GrowthFetchLatestAPI(generics.RetrieveAPIView):
    """
    Returns latest growth.
    """
    serializer_class = D180GrowthSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return (Process.objects.filter(type_id='d180-growth')
                               .order_by('-created')
                               .first())


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
