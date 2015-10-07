# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from project_management.serializers import MilestoneSerializer
from .utility import (IsViewerPermission, IsOwnerPermission,
                      HasMilestoneCreatePermission, CreatePermissionMixin)

from core.models import Process
from core.serializers import ProcessSerializer


class MilestoneListAPIView(CreatePermissionMixin, generics.ListCreateAPIView):

    permission_classes = (HasMilestoneCreatePermission, permissions.IsAuthenticated,)
    serializer_class = MilestoneSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_milestones('viewer')


class MilestoneRetrieveAPIView(generics.RetrieveAPIView):

    permission_classes = (IsViewerPermission, permissions.IsAuthenticated,)
    serializer_class = MilestoneSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_milestones('viewer')


class MilestoneUpdateAPIView(generics.UpdateAPIView):

    permission_classes = (IsOwnerPermission,)
    serializer_class = MilestoneSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_milestones('owner')


class MilestoneProcessListAPIView(generics.ListAPIView):

    permission_classes = (IsOwnerPermission,)
    serializer_class = ProcessSerializer

    def get_queryset(self, *args, **kwargs):
        filter_set = self.request.user.get_milestones('viewer')
        return Process.objects.filter(milestones__in=filter_set)
