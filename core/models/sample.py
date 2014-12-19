# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import AutoUUIDMixin, TimestampMixin
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
        process_tree = ProcessNode(process=None, piece='a')
        sample = self.model(substrate=substrate, comment=comment,
                            process_tree=process_tree)
        sample.save()
        process_tree.save()
        sample.process_tree = process_tree
        sample.save()

        return sample


class Sample(TimestampMixin, AutoUUIDMixin, models.Model):
    prefix = 's'
    padding = 4

    comment = fields.RichTextField(blank=True)
    substrate = models.OneToOneField(Substrate)
    process_tree = mptt.TreeOneToOneField(ProcessNode, null=True)

    objects = SampleManager()

    def _get_tree_queryset(self):
        return ProcessNode.objects.filter(tree_id=self.process_tree.tree_id)

    def _refresh_tree(self):
        self.process_tree = ProcessNode.objects.get(id=self.process_tree_id)

    def _get_next_piece(self):
        used_piece_names = list(self._get_tree_queryset()
            .order_by('-piece').values_list('piece', flat=True))
        return chr(ord(used_piece_names[0]) + 1)

    def _insert_node(self, process, piece, parent, comment=''):
        ProcessNode.objects.create(process=process, piece=piece,
                                   comment=comment, parent_id=parent.id)

    def split(self, number=2, piece='a', comment=None, force_refresh=True):
        """
        Splits the sample piece into the specific number of pieces, with an
        optional comment on the split process itself.
        """
        if comment is None:
            comment = 'Split sample into {0} pieces'.format(number)

        process = SplitProcess.objects.create(comment=comment)

        branch = self.get_piece(piece)
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
            self._insert_node(process, new_piece, branch)
        if force_refresh:  # workaround to force the root node to update
            self._refresh_tree()

    def run_process(self, process, piece='a', comment='', force_refresh=True):
        """
        Append a process to the specified branch.
        """
        branch = self.get_piece(piece)
        self._insert_node(process, piece, branch, comment)
        if force_refresh:  # workaround to force the root node to update
            self._refresh_tree()

    def insert_process_before(self, process, uuid,
                              comment='', force_refresh=True):
        """
        Insert a process into the tree before the specified node.
        """
        pass

    def insert_process_after(self, process, uuid,
                              comment='', force_refresh=True):
        """
        Insert a process into the tree after the specified node.
        """
        pass

    @property
    def leaf_nodes(self):
        """
        Returns all of the leaf nodes of the tree as a list.
        """
        return self._get_tree_queryset().filter(lft=models.F('rght') - 1)

    @property
    def root_node(self):
        """
        Returns the root node of the tree.
        """
        return self.process_tree

    @property
    def pieces(self):
        """
        Returns a list of the pieces the sample is currently using.
        """
        return [n.piece for n in self.leaf_nodes]

    def get_piece(self, piece):
        """
        Branch uid in the format {sample uid}{piece}
        """
        return (self._get_tree_queryset().filter(piece=piece)
                                         .order_by('-level')
                                         .first())

    def get_process_node(self, uuid):
        """
        Get the specific node from the tree with the specified uuid.
        """
        uuid = ProcessNode.strip_uuid(uuid)
        return self._get_tree_queryset().filter(uuid_full__startswith=uuid)

    def get_process(self, uuid):
        """
        Get all nodes from the tree that have the specified process.
        """
        uuid = Process.strip_uuid(uuid)
        return self._get_tree_queryset().filter(process__uuid_full__startswith=uuid)
