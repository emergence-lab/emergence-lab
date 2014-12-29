# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from core.models import Process, ProcessNode
from core.serializers import ProcessSerializer, ProcessNodeSerializer
from .mixins import UUIDRetrieveAPIView


class ProcessListAPIView(generics.ListAPIView):
    """
    Read-only API view to list generic details of all processes.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class ProcessRetrieveAPIView(UUIDRetrieveAPIView):
    """
    Read-only API view to list generic details of a process from the uuid,
    either short or long.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProcessNodeRetrieveAPIView(UUIDRetrieveAPIView):
    """
    Read-only API view to list details of a process node from the uuid,
    either short or long.
    """
    queryset = ProcessNode.objects.all()
    serializer_class = ProcessNodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
