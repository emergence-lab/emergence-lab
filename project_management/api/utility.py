from __future__ import absolute_import

from django.shortcuts import get_object_or_404

from rest_framework import permissions

from core.models import Project, Investigation


class CreatePermissionMixin(object):

    def check_relation_permissions(self, request):
        for permission in self.get_permissions():
            if not hasattr(permission, 'has_relation_permission'):
                return
            if not permission.has_relation_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def create(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        self.check_relation_permissions(request)
        return super(CreatePermissionMixin, self).create(request, *args, **kwargs)


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


class HasInvestigationCreatePermission(permissions.BasePermission):

    def has_relation_permission(self, request, view):
        project = get_object_or_404(Project, id=request.data['project'][0])
        if project.is_owner(request.user):
            return True


class HasMilestoneCreatePermission(permissions.BasePermission):

    def has_relation_permission(self, request, view):
        investigation = get_object_or_404(Investigation, id=request.data['investigation'][0])
        if project.is_owner(request.user):
            return True
