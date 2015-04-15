# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions, views
from rest_framework.response import Response

from core.models import Process, ProcessNode
from core.serializers import (DataFileSerializer, ProcessSerializer,
                              ProcessNodeSerializer,)


class ProcessListAPIView(generics.ListAPIView):
    """
    Read-only API view to list generic details of all processes.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class ProcessRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only API view to show generic details of a process from the uuid,
    either short or long.
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])

        obj = generics.get_object_or_404(queryset, uuid_full__startswith=uuid)

        self.check_object_permissions(self.request, obj)

        return obj


class ProcessNodeRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only API view to show details of a process node from the uuid,
    either short or long.
    """
    queryset = ProcessNode.objects.all()
    serializer_class = ProcessNodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = ProcessNode.strip_uuid(self.kwargs[self.lookup_url_kwarg])

        obj = generics.get_object_or_404(queryset, uuid_full__startswith=uuid)

        self.check_object_permissions(self.request, obj)

        return obj


class ProcessFilesRetrieveAPIView(views.APIView):
    """
    Read-only API view to list the files associated with a process from a uuid,
    either short or long.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        uuid = Process.strip_uuid(kwargs.get('uuid'))
        process = Process.objects.get(uuid_full__startswith=uuid)
        files = process.datafiles.get_queryset()
        return Response([DataFileSerializer(f).data for f in files])
