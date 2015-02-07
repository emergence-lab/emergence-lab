# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions, views
from rest_framework.response import Response

from core.models import Sample, Substrate
from core.serializers import SampleSerializer, SubstrateSerializer, ProcessSerializer


class SubstrateListAPIView(generics.ListAPIView):
    """
    Read-only endpoint to list details for all substrates.
    """
    queryset = Substrate.objects.all()
    serializer_class = SubstrateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class SampleListAPIView(generics.ListAPIView):
    """
    Read-only endpoint to list details for all samples.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class SampleRetrieveAPIView(views.APIView):
    """
    Read-only endpoint to show shallow details for a sample from the uuid.
    Does not retrieve the entire process tree.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _recurse_tree(self, node):
        print('processing node {}'.format(node.uuid))
        data = ProcessSerializer(node.process).data
        data['piece'] = node.piece
        data['children'] = [self._recurse_tree(child)
                            for child in node.get_children()]
        return data

    def get(self, request, *args, **kwargs):
        sample = Sample.objects.get_by_uuid(kwargs.get('uuid'))
        serializer = SampleSerializer(sample)
        data = serializer.data
        node = sample.process_tree
        data['process_tree'] = self._recurse_tree(node)
        return Response(data)
