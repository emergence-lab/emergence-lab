# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from project_management.serializers import ProjectSerializer


class ProjectListAPIView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self, *args, **kwargs):
        return self.request.user.get_projects('viewer')
