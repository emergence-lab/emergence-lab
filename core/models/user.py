# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.contrib.auth import models as auth
from django.contrib.auth import get_backends
from django.core.mail import send_mail
from django.core import validators
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token

from .mixins import ActiveStateMixin
from .project import Project, Milestone, Investigation, ProjectTracking, Task


def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    for backend in get_backends():
        if hasattr(backend, "has_perm"):
            if backend.has_perm(user, perm, obj):
                return True
    return False


def _user_has_module_perms(user, app_label):
    for backend in get_backends():
        if hasattr(backend, "has_module_perms"):
            if backend.has_module_perms(user, app_label):
                return True
    return False


@python_2_unicode_compatible
class User(ActiveStateMixin, auth.AbstractBaseUser):
    """
    A custom user model that stores the name in a more portable way. Also
    stores information relating to project tracking.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[validators.RegexValidator(r'^[\w.@+-]+$',
            _('Enter a valid username.'), 'invalid')])
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    short_name = models.CharField(_('preferred name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    groups = models.ManyToManyField(auth.Group,
        verbose_name=_('groups'), blank=True,
        help_text=_('The groups this user belongs to. A user will get all '
                    'permissions granted to each of their groups.'),
        related_name='custom_users', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(auth.Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_users', related_query_name='custom_user')

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    projects = models.ManyToManyField(Project, through=ProjectTracking,
        verbose_name=_('tracked projects'), blank=True,
        help_text=_('Projects this user is tracking'),
        related_name='users', related_query_name='user')

    objects = auth.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_projects(self, permission, followed=None):
        """
        Returns a queryset of projects that the user has the specified
        permissions on.

        :param permission: Should be one of 'owner', 'member', or 'viewer'
                           depending on the desired permission desired.
        """
        group_ids = self.groups.values_list('id', flat=True)
        if permission == 'owner':
            permission_filters = models.Q(owner_group_id__in=group_ids)
        elif permission == 'member':
            permission_filters = (models.Q(owner_group_id__in=group_ids) |
                                  models.Q(member_group_id__in=group_ids))
        elif permission == 'viewer':
            permission_filters = (models.Q(owner_group_id__in=group_ids) |
                                  models.Q(member_group_id__in=group_ids) |
                                  models.Q(viewer_group_id__in=group_ids))
        else:
            raise ValueError('Permission {} is not valid. Should be one of '
                             'owner, member, or viewer'.format(permission))
        if followed is None:
            return Project.objects.filter(permission_filters).order_by('id')
        elif followed is True:
            return self.projects.filter(permission_filters).order_by('id')
        else:
            project_ids = self.projects.values_list('id', flat=True)
            return (Project.objects.filter(permission_filters)
                                   .exclude(id__in=project_ids)
                                   .order_by('id'))

    def get_investigations(self, permission, followed=None):
        """
        Returns a queryset of investigations that the user has the specified
        permissions on.

        :param permission: Should be one of 'owner', 'member', or 'viewer'
                           depending on the desired permission desired.
        """
        project_ids = self.get_projects(permission,
                                        followed).values_list('id', flat=True)
        return (Investigation.objects.filter(project_id__in=project_ids)
                                     .order_by('id'))

    def get_milestones(self, permission, followed=None):
        """
        Returns a queryset of milestones that the user has the specified
        permissions on.

        :param permission: Should be one of 'owner', 'member', or 'viewer'
                           depending on the desired permission desired.
        """
        investigation_ids = self.get_investigations(permission,
                                                    followed).values_list('id', flat=True)
        return (Milestone.objects.filter(investigation_id__in=investigation_ids)
                                 .order_by('id'))

    def get_tasks(self, permission, followed=None):
        """
        Returns a queryset of milestones that the user has the specified
        permissions on.

        :param permission: Should be one of 'owner', 'member', or 'viewer'
                           depending on the desired permission desired.
        """
        milestone_ids = self.get_milestones(permission,
                                            followed).values_list('id', flat=True)
        return (Task.objects.filter(milestone_id__in=milestone_ids)
                            .order_by('id'))

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


@receiver(models.signals.post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
