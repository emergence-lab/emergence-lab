from __future__ import absolute_import

from rest_framework import permissions


class IsViewerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_viewer(request.user)


class IsMemberPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_member(request.user)


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)
