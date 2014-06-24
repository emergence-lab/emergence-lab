from __future__ import unicode_literals

from django.db import models


class operator(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'operators'


class platter(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    serial = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'platters'


class project(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'projects'


class investigation(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    projects = models.ManyToManyField(project)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'investigations'
