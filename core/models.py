from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class active_manager(models.Manager):
    """
    Manager to filter on the ``active`` field.
    """
    def get_queryset(self):
        return super(active_manager, self).get_queryset().filter(active=True)


class inactive_manager(models.Manager):
    """
    Manager to filter on the ``active`` field.
    """
    def get_queryset(self):
        return super(inactive_manager, self).get_queryset().filter(active=False)


class platter(models.Model):
    """
    Stores platter information.
    """
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    serial = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    objects = models.Manager()
    current = active_manager()
    retired = inactive_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'platters'


class project(models.Model):
    """
    Stores information on a project, which is a higher level organizational tool.
    """
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    objects = models.Manager()
    current = active_manager()
    retired = inactive_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'projects'


class investigation(models.Model):
    """
    Stores information on an individual investigation related to one or more projects.
    """
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    projects = models.ManyToManyField(project)

    objects = models.Manager()
    current = active_manager()
    retired = inactive_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'investigations'


class operator(models.Model):
    """
    Stores operator information.
    """
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User)
    projects = models.ManyToManyField(project)

    objects = models.Manager()
    current = active_manager()
    retired = inactive_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'operators'
