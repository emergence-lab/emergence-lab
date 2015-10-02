# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from project_management.serializers import ProjectSerializer
from .utility import IsViewerPermission, IsOwnerPermission

from core.models import Project


class ProjectListAPIView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('viewer')

    def perform_create(self, serializer):
        obj = serializer.save()
        self.request.user.groups.add(obj.owner_group)


class ProjectRetrieveAPIView(generics.RetrieveAPIView):

    permission_classes = (IsViewerPermission,)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('viewer')


class ProjectUpdateAPIView(generics.UpdateAPIView):

    permission_classes = (IsOwnerPermission,)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('owner')
