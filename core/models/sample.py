# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import string

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

    def create(self, substrate, comment=''):
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
    """
    Class representing a sample, which is an organizational unit representing
    a single piece of material, chemical mixture, etc. on which experimentation
    is done.
    """
    prefix = 's'
    padding = 4

    comment = fields.RichTextField(blank=True)
    substrate = models.OneToOneField(Substrate)
    process_tree = mptt.TreeOneToOneField(ProcessNode, null=True)

    objects = SampleManager()

    def _get_tree_queryset(self):
        return ProcessNode.objects.filter(tree_id=self.process_tree.tree_id)

    def _get_next_piece(self):
        used_piece_names = set(self._get_tree_queryset()
            .order_by('-piece').values_list('piece', flat=True))
        possible_pieces = list(set(string.ascii_lowercase) - used_piece_names)
        return sorted(possible_pieces)[0]

    def _insert_node(self, process, piece, parent, comment=''):
        return ProcessNode.objects.create(process=process, piece=piece,
                                          comment=comment, parent_id=parent.id)

    def refresh_tree(self):
        """
        Force the root node of the tree to refresh to correct incorrect
        calculations or references due to it being out of date.
        """
        self.process_tree = ProcessNode.objects.get(id=self.process_tree_id)

    def split(self, number=2, piece='a', comment=None, force_refresh=True):
        """
        Splits the sample piece into the specific number of pieces, with an
        optional comment on the split process itself.
        """
        if comment is None:
            comment = 'Split sample into {0} pieces'.format(number)

        process = SplitProcess.objects.create(comment=comment)
        nodes = []

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
            nodes.append(self._insert_node(process, new_piece, branch))
        if force_refresh:  # workaround to force the root node to update
            self.refresh_tree()
        return nodes

    def run_process(self, process, piece='a', comment='', force_refresh=True):
        """
        Append a process to the specified branch.
        """
        branch = self.get_piece(piece)
        node = self._insert_node(process, piece, branch, comment)
        if force_refresh:  # workaround to force the root node to update
            self.refresh_tree()
        return node

    def insert_process_before(self, process, uuid,
                              comment='', force_refresh=True):
        """
        Insert a process into the tree before the specified node. Invalidates
        references for affected nodes.
        """
        target = self.get_node(uuid)
        if target == self.root_node:
            raise Exception('Error: Cannot insert before the root node.')

        parent = target.parent
        children = list(target.get_siblings(include_self=True))
        node = ProcessNode.objects.create(process=process, piece=parent.piece,
                                          comment=comment, parent_id=parent.id)
        for child in children:
            child.parent = node
            child.save()

        if force_refresh:
            self.refresh_tree()
        return node

    def insert_process_after(self, process, uuid,
                              comment='', force_refresh=True):
        """
        Insert a process into the tree after the specified node. Invalidates
        references for affected nodes.
        """
        parent = self.get_node(uuid)
        children = list(parent.get_children())
        node = ProcessNode.objects.create(process=process, piece=parent.piece,
                                          comment=comment, parent_id=parent.id)
        for child in children:
            child.parent = node
            child.save()

        if force_refresh:
            self.refresh_tree()
        return node

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
        return sorted([n.piece for n in self.leaf_nodes])

    @property
    def node_count(self):
        """
        Returns the number of nodes in the tree including the root.
        """
        return self.process_tree.get_descendant_count() + 1

    def get_piece(self, piece):
        """
        Branch uid in the format {sample uid}{piece}
        """
        return self.leaf_nodes.get(piece=piece)

    def get_node(self, uuid):
        """
        Get the specific node from the tree with the specified uuid.
        """
        uuid = ProcessNode.strip_uuid(uuid)
        return self._get_tree_queryset().get(uuid_full__startswith=uuid)

    def get_nodes_for_process(self, uuid):
        """
        Get all nodes from the tree that have the specified process.
        """
        uuid = Process.strip_uuid(uuid)
        return self._get_tree_queryset().filter(process__uuid_full__startswith=uuid)
