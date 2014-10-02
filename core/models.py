from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.conf import settings
from django.contrib import auth
from django.core import validators
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


# Temporary duplication of django.contrib.auth.models code to try to more
# smoothly transition to a custom user model. core.User will live alongside
# core.operator and auth.User for the moment with auth.User being the value of
# settings.AUTH_USER_MODEL. Eventually, we will switch all foreign keys to use
# core.User instead of core.operator. Once that is complete, we will switch over
# to core.User instead of auth.User. User data will be manually migrated over.

def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    for backend in auth.get_backends():
        if hasattr(backend, "has_perm"):
            if backend.has_perm(user, perm, obj):
                return True
    return False


def _user_has_module_perms(user, app_label):
    for backend in auth.get_backends():
        if hasattr(backend, "has_module_perms"):
            if backend.has_module_perms(user, app_label):
                return True
    return False


class User(auth.models.AbstractBaseUser):
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
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    groups = models.ManyToManyField(auth.models.Group,
        verbose_name=_('groups'), blank=True,
        help_text=_('The groups this user belongs to. A user will get all '
                    'permissions granted to each of their groups.'),
        related_name='custom_users', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(auth.models.Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_users', related_query_name='custom_user')

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    projects = models.ManyToManyField('project', through='ProjectTracking',
        verbose_name=_('tracked projects'), blank=True,
        help_text=_('Projects this user is tracking'),
        related_name='users', related_query_name='user')

    objects = auth.models.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

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


class ActiveStateManager(models.Manager):
    """
    Manager to filter on the ``active`` field.
    """
    def __init__(self, active_test):
        super(ActiveStateManager, self).__init__()
        self.active_test = active_test

    def get_queryset(self):
        return (super(ActiveStateManager, self)
                    .get_queryset().filter(is_active=self.active_test))


class ActiveStateMixin(models.Model):
    """
    Mixin for models that keep an active/inactive state.
    """
    is_active = models.BooleanField(_('active'), default=True)
    status_changed = models.DateTimeField(_('status changed'), null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveStateManager(active_test=True)
    inactive_objects = ActiveStateManager(active_test=False)

    class Meta:
        abstract = True

    def activate(self, save=True):
        """
        Activate the object, raise an exception if it was already active.
        """
        if self.is_active:
            raise Exception('{0} was already active'.format(self._meta.verbose_name))
        self.is_active = True
        self.status_changed = timezone.now()
        if save:
            self.save()

    def deactivate(self, save=True):
        """
        Deactivate the object, raise an exception if it was already active.
        """
        if not self.is_active:
            raise Exception('{0} was already not active'.format(self._meta.verbose_name))
        self.is_active = False
        self.status_changed = timezone.now()
        if save:
            self.save()


class TimestampMixin(models.Model):
    """
    Mixin for models that keeps track of when an object was created or modified.
    """
    created = models.DateTimeField(_('date created'), auto_now_add=True)
    modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class platter(ActiveStateMixin, models.Model):
    """
    Stores platter information.
    """
    name = models.CharField(_('name'), max_length=45)
    serial = models.CharField(_('serial number'), max_length=20, blank=True)
    start_date = models.DateField(_('date started'), auto_now_add=True)

    class Meta:
        verbose_name = _('platter')
        verbose_name_plural = _('platters')
        db_table = 'platters'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class project(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information on a project, which is a higher level organizational
    tool.
    """
    name = models.CharField(_('name'), max_length=45)
    slug = AutoSlugField(_('slug'), populate_from='name')
    core = models.BooleanField(_('core project'), default=False)
    description = RichTextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        db_table = 'projects'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class investigation(ActiveStateMixin, TimestampMixin, models.Model):
    """
    Stores information on an individual investigation related to one or more
    projects.
    """
    name = models.CharField(_('name'), max_length=45)
    slug = AutoSlugField(_('slug'), populate_from='name')
    description = RichTextField(_('description'), blank=True)
    project = models.ForeignKey(project)

    class Meta:
        verbose_name = _('investigation')
        verbose_name_plural = _('investigations')
        db_table = 'investigations'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class operator(ActiveStateMixin, models.Model):
    """
    Stores operator information.
    """
    name = models.CharField(max_length=45)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    projects = models.ManyToManyField(project, through='project_tracking')

    class Meta:
        verbose_name = _('operator')
        verbose_name_plural = _('operators')
        db_table = 'operators'

    def __str__(self):
        return self.name


class ProjectTracking(models.Model):
    """
    Stores ownership and tracking information for projects.
    """
    project = models.ForeignKey(project)
    user = models.ForeignKey(User)
    is_owner = models.BooleanField(default=False)

    class Meta:
        db_table = 'project_tracking'


class project_tracking(models.Model):
    """
    Stores ownership and tracking information for projects.
    """
    project = models.ForeignKey(project)
    operator = models.ForeignKey(operator)
    is_pi = models.BooleanField(default=False)

    class Meta:
        db_table = 'project_operator_tracking'
