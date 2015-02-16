# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions, views
from rest_framework.response import Response

from core.models import Sample, Substrate, ProcessNode
from core.serializers import (SampleSerializer, SubstrateSerializer,
                              ProcessNodeSerializer)


class SubstrateListAPIView(generics.ListAPIView):
    """
    Read-only endpoint to list details for all substrates.
    """
    queryset = Substrate.objects.all()
    serializer_class = SubstrateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class SampleRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only endpoint to show details for a sample from the uuid.
    Lists uuids of process nodes.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Sample.strip_uuid(self.kwargs[self.lookup_url_kwarg])

        obj = generics.get_object_or_404(queryset, pk=uuid)

        self.check_object_permissions(self.request, obj)

        return obj


class SampleListAPIView(generics.ListAPIView):
    """
    Read-only endpoint to list details for all samples.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class SampleNodeRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only API view to show details of a process node from the uuid,
    either short or long.
    """
    queryset = ProcessNode.objects.all()
    serializer_class = ProcessNodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'node_uuid'

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


class SampleTreeNodeAPIView(views.APIView):
    """
    Read-only endpoint to show details for a sample from the uuid.
    Retrieves the entire process tree.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _recurse_tree(self, node):
        data = ProcessNodeSerializer(node).data
        data['children'] = [self._recurse_tree(child)
                            for child in node.get_children()]
        return data

    def get(self, request, *args, **kwargs):
        sample = Sample.objects.get_by_uuid(kwargs.get('uuid'))
        data = SampleSerializer(sample).data
        data['nodes'] = self._recurse_tree(sample.process_tree)
        return Response(data)


class SampleLeafNodeAPIView(views.APIView):
    """
    Read-only endpoint to show the leaf nodes for a sample from the uuid.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        sample = Sample.objects.get_by_uuid(kwargs.get('uuid'))
        piece = kwargs.get('piece')
        data = SampleSerializer(sample).data
        data['nodes'] = [ProcessNodeSerializer(node).data
                         for node in sample.leaf_nodes
                         if piece is None or node.piece == piece]
        return Response(data)


class SamplePieceNodeAPIView(views.APIView):
    """
    Read-only endpoint to show details for a sample from the uuid.
    Retrieves the entire process tree for the specified piece.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _recurse_tree(self, node, piece):
        data = ProcessNodeSerializer(node).data
        data['children'] = [self._recurse_tree(child, piece)
                            for child in node.get_children()
                            if child.piece == piece]
        return data

    def get(self, request, *args, **kwargs):
        sample = Sample.objects.get_by_uuid(kwargs.get('uuid'))
        data = SampleSerializer(sample).data
        data['nodes'] = self._recurse_tree(sample.process_tree,
                                           kwargs.get('piece'))
        return Response(data)
