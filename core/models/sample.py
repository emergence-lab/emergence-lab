# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin
from .process import Process, ProcessNode
from core import fields


@python_2_unicode_compatible
class Substrate(polymorphic.PolymorphicModel, TimestampMixin):
    """
    Base class for all substrates.
    """
    comment = fields.RichTextField(blank=True)
    source = models.CharField(max_length=100, blank=True)
    serial = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.serial


class SampleManager(models.Manager):

    def _create_sample(self, uid, substrate, process_tree):
        pass

    def create_sample(self, substrate, comment='', process=None):
        uid = self.model._generate_uid()
        if process is None:
            process_tree = None
        else:
            process_tree = ProcessNode.objects.create(process=process,
                                                      piece='a')
        sample = self.model(uid=uid, substrate=substrate, comment=comment,
                            process_tree=process_tree)
        sample.save()
        return sample


@python_2_unicode_compatible
class Sample(TimestampMixin, models.Model):
    uid = models.SlugField(max_length=25)
    comment = fields.RichTextField(blank=True)
    substrate = models.OneToOneField(Substrate)
    process_tree = mptt.TreeOneToOneField(ProcessNode, null=True)

    objects = SampleManager()

    def __str__(self):
        return self.uid

    @classmethod
    def _generate_uid(cls):
        count = str(cls.objects.all().count() + 1).zfill(4)
        return 'smpl-{0}'.format(count)

    def get_pieces(self):
        pass

    def get_num_pieces(self):
        pass

    def split_sample(self, number=2, comment=None):
        if self.process_tree is None:
            dummy = Process.objects.create(uid=self.uid, comment='dummy')
            self.process_tree = ProcessNode.objects.create(process=dummy)
        if comment is None:
            comment = 'Split sample into {0} pieces'.format(number)
        process = Process.objects.create(uid='split-0001', comment=comment)
        for i in range(number):
            node = ProcessNode(parent=self.process_tree, process=process)
            node.insert_at(self.process_tree, save=True)

    def get_branch(self, uid):
        pass

    def get_process_node(self, uid):
        pass

    def get_process(self, uid):
        pass
