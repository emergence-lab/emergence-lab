# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions, views
from rest_framework.response import Response

from project_management.serializers import ProjectSerializer
from .utility import IsViewerPermission, IsOwnerPermission

from core.models import Project, ProjectTracking


class ProjectListAllAPIView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('viewer')

    def perform_create(self, serializer):
        obj = serializer.save()
        self.request.user.groups.add(obj.owner_group)


class ProjectListFollowedAPIView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('viewer', followed=True)

    def perform_create(self, serializer):
        obj = serializer.save()
        self.request.user.groups.add(obj.owner_group)


class ProjectRetrieveAPIView(generics.RetrieveAPIView):

    permission_classes = (IsViewerPermission, permissions.IsAuthenticated,)
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


class ProjectTrackAPIView(views.APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(slug=kwargs.get('slug'))
        ProjectTracking.objects.get_or_create(project=project,
                                              user=self.request.user,
                                              defaults={'is_owner': False})
        data = ProjectSerializer(project).data
        return Response(data)


class ProjectUntrackAPIView(views.APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(slug=kwargs.get('slug'))
        tracking = ProjectTracking.objects.filter(project=project,
                                                  user=self.request.user)
        if tracking.count():
            tracking.delete()
        data = ProjectSerializer(project).data
        return Response(data)
