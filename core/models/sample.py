# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import TimestampMixin, AutoUIDMixin
from .process import Process, ProcessNode, SplitProcess
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

    def create_sample(self, substrate, comment=''):
        """
        Creates a sample with a default 'root' processnode which makes it easy
        to refer to the root node.
        """
        root_process = Process.objects.create(uid='root')
        process_tree = ProcessNode(process=root_process, piece='a')
        sample = self.model(substrate=substrate, comment=comment,
                            process_tree=process_tree)
        sample.save()
        process_tree.save()
        sample.process_tree = process_tree
        sample.save()

        return sample


class Sample(AutoUIDMixin, TimestampMixin, models.Model):
    prefix = 'smpl-'

    comment = fields.RichTextField(blank=True)
    substrate = models.OneToOneField(Substrate)
    process_tree = mptt.TreeOneToOneField(ProcessNode, null=True)

    objects = SampleManager()

    def _get_tree_queryset(self):
        return ProcessNode.objects.filter(tree_id=self.process_tree.tree_id)

    def _get_next_piece(self):
        used_piece_names = list(self._get_tree_queryset()
            .order_by('-piece').values_list('piece', flat=True))
        return chr(ord(used_piece_names[0]) + 1)

    def split(self, number=2, piece='a', comment=None):
        """

        """
        if comment is None:
            comment = 'Split sample into {0} pieces'.format(number)

        process = SplitProcess.objects.create(comment=comment)

        branch = self.get_branch(piece)
        for i in range(number):
            if i == 0:
                new_piece = piece
            else:
                new_piece = self._get_next_piece()
            # Note: Issue #248 in django-mptt causes the tree to not be properly
            #       updated when inserting objects if parent is set. Workaround
            #       is to set parent_id instead. This fixes methods such as
            #       MPTTModel.get_descendants(). Since you are referencing an
            #       object that has changed in the database (process_tree),
            #       the lft and rght items are not updated properly. Workarounds
            #       include manually updating the root node or requerying for
            #       the sample object which will force a refresh.
            ProcessNode.objects.create(process=process,
                                       piece=new_piece,
                                       parent_id=branch.id)
        # workaround to force the root node to update
        self.process_tree = ProcessNode.objects.get(id=self.process_tree_id)

    def get_tree(self):
        return self.process_tree

    def run_process(self, process, piece='a'):
        branch = self.get_branch(piece)
        ProcessNode.objects.create(process=process, piece=piece,
                                   parent_id=branch.id)
        self.process_tree = ProcessNode.objects.get(id=self.process_tree_id)

    def get_pieces(self):
        pass

    def get_branch(self, piece):
        """
        Branch uid in the format {sample uid}{piece}
        """
        return (self._get_tree_queryset().filter(piece=piece)
                                         .order_by('-level')
                                         .first())

    def get_process_node(self, node_uid):
        pass

    def get_process(self, process_uid):
        return ProcessNode.objects.filter(tree_id=self.process_tree.tree_id,
                                          process__uid=process_uid)
