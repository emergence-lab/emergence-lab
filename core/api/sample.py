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
    Read-only endpoint to show details for a sample from the uuid.
    Retrieves the entire process tree.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _recurse_tree(self, node):
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

class SampleLeafNodesAPIView(views.APIView):
    """
    Read-only endpoint to show the leaf nodes for a sample from the uuid.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        sample = Sample.objects.get_by_uuid(kwargs.get('uuid'))
        serializer = SampleSerializer(sample)
        data = serializer.data
        del data['process_tree']
        data['leaf_nodes'] = []
        for node in sample.leaf_nodes:
            process = ProcessSerializer(node.process).data
            process['piece'] = node.piece
            data['leaf_nodes'].append(process)
        return Response(data)
