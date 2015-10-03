# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import Q

from rest_framework import generics, permissions

from project_management.serializers import InvestigationSerializer
from .utility import IsViewerPermission, IsOwnerPermission

from core.models import Process
from core.serializers import ProcessSerializer


class InvestigationListAPIView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvestigationSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_investigations('viewer')


class InvestigationRetrieveAPIView(generics.RetrieveAPIView):

    permission_classes = (IsViewerPermission,)
    serializer_class = InvestigationSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_investigations('viewer')


class InvestigationUpdateAPIView(generics.UpdateAPIView):

    permission_classes = (IsOwnerPermission,)
    serializer_class = InvestigationSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_investigations('owner')


class InvestigationProcessListAPIView(generics.ListAPIView):

    permission_classes = (IsOwnerPermission,)
    serializer_class = ProcessSerializer

    def get_queryset(self, *args, **kwargs):
        filter_set = Q(investigations__in=self.request.user.get_investigations('viewer'))
        return Process.objects.filter(filter_set)
