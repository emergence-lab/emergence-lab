# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from core.models import User
from core.serializers import UserSerializer


class UserListAPIView(generics.ListAPIView):
    """
    Read-only API View to list all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100
