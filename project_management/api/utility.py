from __future__ import absolute_import

from django.shortcuts import get_object_or_404

from rest_framework import permissions

from core.models import Project, Investigation


class CreatePermissionMixin(object):
    """
    Mixin to check against custom permission class.
    Checks that the foreign key relation of the to-be-created object has the proper permission.
    """

    def check_relation_permissions(self, request):
        for permission in self.get_permissions():
            if not hasattr(permission, 'has_relation_permission'):
                return
            if not permission.has_relation_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def create(self, request, *args, **kwargs):
        self.check_relation_permissions(request)
        return super(CreatePermissionMixin, self).create(request, *args, **kwargs)


class IsViewerPermission(permissions.BasePermission):
    """
    Checks if the user is a viewer and that the method is read-only.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_viewer(request.user)


class IsMemberPermission(permissions.BasePermission):
    """
    Checks if the user is a member.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_member(request.user)


class IsOwnerPermission(permissions.BasePermission):
    """
    Checks if the user is an owner.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)


class HasInvestigationCreatePermission(permissions.BasePermission):
    """
    Checks if the user is an owner of the project for a created investigation.
    """

    def has_relation_permission(self, request, view):
        project = get_object_or_404(Project, id=request.data['project'])
        if project.is_owner(request.user):
            return True


class HasMilestoneCreatePermission(permissions.BasePermission):
    """
    Checks if the user is an owner of the investigation for a created milestone.
    """

    def has_relation_permission(self, request, view):
        investigation = get_object_or_404(Investigation, id=request.data['investigation'])
        if investigation.is_owner(request.user):
            return True
