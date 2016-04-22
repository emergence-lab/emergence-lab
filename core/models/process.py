# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.core.files.storage import default_storage as labshare
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

from actstream import action
from mptt import models as mptt
from polymorphic.models import PolymorphicModel
from simple_history import models as simple_history

from core.models.mixins import TimestampMixin, UUIDMixin
from core.models import fields, Investigation, Milestone


def get_file_path(instance, filename):
    """
    Stores files in /process_data and generates a UUID-based file name
    """
    return os.path.join('processes', instance.process.uuid_full.hex, filename)


@python_2_unicode_compatible
class ProcessCategory(models.Model):
    """Holds information about the category of process types."""

    slug = models.SlugField(primary_key=True, max_length=100, default='uncategorized')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.slug)

    def __str__(self):
        return self.name

    def processtype_slugs(self):
        return self.processtypes.values_list('type', flat=True)


@python_2_unicode_compatible
class ProcessType(models.Model):
    """
    Holds information about types of processes.
    """
    SCHEDULING_TYPE = (
        ('none', 'None'),
        ('simple', 'Simple'),
        ('full', 'Full'),
        ('external', 'External'),
    )

    CREATION_TYPE = (
        ('default', 'Default'),
        ('custom', 'Custom'),
    )

    type = models.SlugField(primary_key=True, max_length=100, default='generic-process')
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    is_destructive = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    scheduling_type = models.CharField(max_length=10, choices=SCHEDULING_TYPE,
                                       default='none')
    creation_type = models.CharField(max_length=10, choices=CREATION_TYPE,
                                     default='default')
    category = models.ForeignKey(ProcessCategory, default='uncategorized',
                                 related_name='processtypes',
                                 related_query_name='processtype')

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.full_name


class ProcessTypeManager(models.Manager):
    """
    Manager to filter on the ``type`` field.
    """
    def __init__(self, process_type):
        super(ProcessTypeManager, self).__init__()
        self.process_type = process_type

    def get_queryset(self):
        return (super(ProcessTypeManager, self)
                    .get_queryset().filter(type_id=self.process_type))


class Process(UUIDMixin, TimestampMixin, models.Model):
    """
    A process represents anything done to a sample which results in data
    (numerical or visual) or alters the properties of the sample.
    """
    prefix = 'p'

    title = models.CharField(max_length=80)
    comment = fields.RichTextField(blank=True)
    legacy_identifier = models.SlugField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             limit_choices_to={'is_active': True})
    type = models.ForeignKey(ProcessType, default='generic-process')

    investigations = models.ManyToManyField(Investigation,
        related_name='processes', related_query_name='process',)
    milestones = models.ManyToManyField(Milestone,
        related_name='processes', related_query_name='milestone',)

    history = simple_history.HistoricalRecords()

    objects = models.Manager()
    generic = ProcessTypeManager(process_type='generic-process')
    split = ProcessTypeManager(process_type='split-process')

    @property
    def samples(self):
        """
        Retrieve a queryset of samples that have the process run on them.
        """
        from core.models import Sample
        trees = ProcessNode.objects.filter(process=self).values_list('tree_id', flat=True)
        nodes = (ProcessNode.objects.filter(tree_id__in=trees,
                                            sample__isnull=False)
                                    .values_list('sample', flat=True))
        return Sample.objects.filter(id__in=nodes).distinct()

    @property
    def nodes(self):
        return self.processnode_set.all()


class ProcessNode(mptt.MPTTModel, UUIDMixin, TimestampMixin):
    """
    Model representing the nodes in a tree of various processes done to
    a sample.
    """
    prefix = 'n'

    comment = fields.RichTextField(blank=True)
    parent = mptt.TreeForeignKey('self', null=True, related_name='children')
    process = models.ForeignKey(Process, null=True)
    piece = models.CharField(max_length=5)
    number = models.IntegerField(default=1)

    objects = mptt.TreeManager()

    def get_sample(self):
        return self.get_root().sample


class DataFile(PolymorphicModel, TimestampMixin):
    """
    Generic model for files associated with processes
    """
    partial_template = 'core/generic_file_partial.html'

    DATA_STATE = [
        ('raw', 'Raw'),
        ('cleaned', 'Cleaned'),
        ('extracted', 'Extracted'),
        ('analyzed', 'Analyzed'),
        ('other', 'Other')
    ]
    CONTENT_TYPE = [
        ('', 'Unknown'),
        ('application/octet-stream', 'Binary File'),
        ('application/pdf', 'PDF File'),
        ('application/vnd.ms-excel', 'Excel File'),
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Excel File'),
        ('image/png', 'PNG Image'),
        ('image/bmp', 'BMP Image'),
        ('image/jpeg', 'JPEG Image'),
        ('image/tiff', 'TIFF Image'),
        ('image/gif', 'GIF Image'),
        ('text/plain', 'Plaintext File'),
        ('text/csv', 'CSV File'),
    ]

    process = models.ForeignKey(Process,
                                related_name='datafiles',
                                related_query_name='datafiles',
                                null=True)
    content_type = models.CharField(max_length=200, blank=True, choices=CONTENT_TYPE, default='')
    data = models.FileField(upload_to=get_file_path, storage=labshare,
                            max_length=200, blank=True, null=True)
    state = models.CharField(max_length=20, choices=DATA_STATE, default='raw')


class ProcessTemplate(TimestampMixin, models.Model):
    """
    Model for templating existing process details for later reference
    """
    process = models.ForeignKey(Process,
                                related_name='templates',
                                related_query_name='templates')
    name = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=80)
    comment = fields.RichTextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                         limit_choices_to={'is_active': True})


@receiver(models.signals.m2m_changed, sender=Process.investigations.through)
def process_actstream(sender, instance=None, created=False, **kwargs):
    for investigation in instance.investigations.all():
        action.send(instance.user,
                    verb='created',
                    action_object=instance,
                    target=investigation)
