# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import operator
import string

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mptt import models as mptt
import polymorphic

from .mixins import AutoUUIDMixin, TimestampMixin
from .process import Process, ProcessNode, SplitProcess
from . import fields


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

    def get_queryset(self):
        return SampleQuerySet(self.model, using=self._db)

    def get_by_uuid(self, uuid, clean=True):
        return self.get_queryset().get_by_uuid(uuid, clean)

    def filter_process(self, **kwargs):
        return self.get_queryset().filter_process(**kwargs)

    def by_process(self, uuid, clean=True):
        return self.get_queryset().by_process(uuid, clean)

    def by_process_type(self, process_type):
        return self.get_queryset().by_process_type(process_type)

    def by_process_types(self, process_types, combine_and=False):
        return self.get_queryset().by_process_types(process_types, combine_and)


class SampleQuerySet(models.query.QuerySet):

    def get_by_uuid(self, uuid, clean=True):
        if clean:
            try:
                uuid, _ = Sample.strip_uuid(uuid)
            except ValueError:
                raise ValueError('Sample UUID {} is ill-formed'.format(uuid))
        if not uuid:
            raise Sample.DoesNotExist
        return self.get(pk=uuid)

    def filter_process(self, **kwargs):
        """
        Generic filtering on processes run on the sample. Keyword arguments
        should be formatted as if it was filtering on the Process model.
        Extra kwargs are as follows:
            - uuid: The short or long uuid of the process
            - type: A single Process (sub)classes
        """
        if 'uuid' in kwargs:
            kwargs['uuid'] = Process.strip_uuid(kwargs['uuid'])
        if 'type' in kwargs:
            kwargs['polymorphic_ctype'] = ContentType.objects.get_for_models(kwargs.pop('type'))

        kwargs = {'process__{}'.format(k): v for k, v in kwargs.items()}

        trees = (ProcessNode.objects.filter(**kwargs)
                                    .order_by('tree_id')
                                    .values_list('tree_id', flat=True)
                                    .distinct())
        return self.filter(process_tree__tree_id__in=trees)

    def by_process(self, uuid, clean=True):
        if clean:
            uuid = Process.strip_uuid(uuid)
        trees = (ProcessNode.objects.filter(process__uuid_full__startswith=uuid)
                                    .order_by('tree_id')
                                    .values_list('tree_id', flat=True)
                                    .distinct())
        return self.filter(process_tree__tree_id__in=trees)

    def by_process_type(self, process_type):
        if process_type != Process and Process not in process_type.__bases__:
            raise ValueError('{} is not a valid process, it does not inherit '
                             'from Process'.format(process_type.__name__))
        content_type = ContentType.objects.get_for_model(process_type)

        trees = (ProcessNode.objects.filter(process__polymorphic_ctype=content_type)
                                    .order_by('tree_id')
                                    .values_list('tree_id', flat=True)
                                    .distinct())
        return self.filter(process_tree__tree_id__in=trees)

    def by_process_types(self, process_types, combine_and=False):
        for process_type in process_types:
            if process_type != Process and Process not in process_type.__bases__:
                raise ValueError('{} is not a valid process, it does not inherit '
                                 'from Process'.format(process_type.__name__))
        content_types = ContentType.objects.get_for_models(*process_types)

        trees = (ProcessNode.objects.filter(process__polymorphic_ctype=content_type)
                                    .order_by('tree_id')
                                    .values_list('tree_id', flat=True)
                                    .distinct()
                 for process_type, content_type in content_types.items())
        q_filters = (models.Q(process_tree__tree_id__in=tree) for tree in trees)
        op = operator.and_ if combine_and else operator.or_

        return self.filter(reduce(op, q_filters))


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

    @classmethod
    def strip_uuid(cls, uuid):
        piece = None
        if isinstance(uuid, int) or not uuid:
            return (uuid, piece)

        if uuid[-1].isalpha():
            piece = uuid[-1]
            uuid = uuid[:-1]

        return (int(uuid[len(cls.prefix):]), piece)

    def _get_tree_queryset(self):
        return ProcessNode.objects.filter(tree_id=self.process_tree.tree_id)

    def _get_next_piece(self):
        used_piece_names = set(self._get_tree_queryset()
            .order_by('-piece').values_list('piece', flat=True))
        possible_pieces = list(set(string.ascii_lowercase) - used_piece_names)
        return sorted(possible_pieces)[0]

    def _insert_node(self, process, piece, number, parent, comment=''):
        return ProcessNode.objects.create(process=process, piece=piece, number=number,
                                          comment=comment, parent_id=parent.id)

    def refresh_tree(self):
        """
        Force the root node of the tree to refresh to correct incorrect
        calculations or references due to it being out of date.
        """
        self.process_tree = ProcessNode.objects.get(id=self.process_tree_id)

    def split(self, user, number=2, piece='a', comment=None, force_refresh=True):
        """
        Splits the sample piece into the specific number of pieces, with an
        optional comment on the split process itself.

        :param user: The user that split the sample.
        :param number: The number of pieces to split the sample into.
        :param piece: The piece to split. Defaults to 'a'.
        :param comment: An optional comment associated with the split.
        :param force_refresh: Specifies whether to update the sample in-place
                              with the new tree. Set to True if the sample
                              variable is going to be used further. Defaults to
                              True.
        :returns: The ProcessNodes associated with the split. One for each
                  piece.
        """
        if comment is None:
            comment = 'Split sample into {0} pieces'.format(number)

        process = SplitProcess.objects.create(comment=comment, user=user)
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
            nodes.append(self._insert_node(process, new_piece, i + 1, branch))
        if force_refresh:  # workaround to force the root node to update
            self.refresh_tree()
        return nodes

    def run_process(self, process, piece='a', number=1, comment='', force_refresh=True):
        """
        Append a process to the specified branch.

        :param process: The process to run on the sample.
        :param piece: The piece to use for the process. Defaults to 'a'.
        :param number: The sample number for the process. Defaults to 1.
        :param comment: An optional comment associated with the process for this
                        sample. Separate from the process comment.
        :param force_refresh: Specifies whether to update the sample in-place
                              with the new tree. Set to True if the sample
                              variable is going to be used further. Defaults to
                              True.
        :returns: The ProcessNode associated with the process.
        """
        branch = self.get_piece(piece)
        node = self._insert_node(process, piece, number, branch, comment)
        if force_refresh:  # workaround to force the root node to update
            self.refresh_tree()
        return node

    def insert_process_before(self, process, uuid,
                              comment='', force_refresh=True):
        """
        Insert a process into the tree before the specified node. Invalidates
        references for affected nodes.

        :param process: The process to run on the sample.
        :param uuid: The uuid of the node to insert the process before. Must be
                     a child node of the sample, cannot be the root node.
        :param comment: An optional comment associated with the process for this
                        sample. Separate from the process comment.
        :param force_refresh: Specifies whether to update the sample in-place
                              with the new tree. Set to True if the sample
                              variable is going to be used further. Defaults to
                              True.
        :returns: The ProcessNode associated with the process.
        :raises Exception: If the provided node is the root node.
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

        :param process: The process to run on the sample.
        :param uuid: The uuid of the node to insert the process after. Must be
                     a child node of the sample.
        :param comment: An optional comment associated with the process for this
                        sample. Separate from the process comment.
        :param force_refresh: Specifies whether to update the sample in-place
                              with the new tree. Set to True if the sample
                              variable is going to be used further. Defaults to
                              True.
        :returns: The ProcessNode associated with the process.
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
    def nodes(self):
        """
        Returns a queryset of the nodes currently associated with the sample.
        """
        return self._get_tree_queryset()

    @property
    def leaf_nodes(self):
        """
        Returns all of the leaf nodes of the tree as a list.
        """
        return self.nodes.filter(lft=models.F('rght') - 1)

    @property
    def root_node(self):
        """
        Returns the root node of the tree.
        """
        return self.process_tree

    @property
    def pieces(self):
        """
        Returns a queryset of the pieces the sample is currently using.
        """
        return (self.leaf_nodes.order_by('piece')
                               .values_list('piece', flat=True))

    @property
    def processes(self):
        """
        Returns a queryset of distinct processes run on the sample.
        """
        nodes = (self.nodes.exclude(process__isnull=True)
                           .values_list('process_id', flat=True))
        return Process.objects.filter(id__in=nodes).distinct()

    @property
    def node_count(self):
        """
        Returns the number of nodes in the tree including the root.
        """
        return self.process_tree.get_descendant_count() + 1

    def get_piece(self, piece, full=False):
        """
        Branch uid in the format {sample uid}{piece}

        :param piece: The piece to retrieve.
        :param full: Whether to retrieve the entire tree to the root for the
                     piece. Defaults to False.
        :returns: Either the leaf node or the entire tree for the specified
                  branch depending on the full parameter.
        """
        if full:
            return (self.leaf_nodes
                        .get(piece=piece)
                        .get_ancestors(include_self=True))
        return self.leaf_nodes.get(piece=piece)

    def get_node(self, uuid, clean=True):
        """
        Get the specific node from the tree with the specified uuid.

        :param uuid: The uuid of the node to retrieve. Must be a child node of
                     the sample.
        :param clean: Whether to clean the provided uuid. Defaults to True.
        :returns: The node with the specified uuid.
        """
        if clean:
            uuid = ProcessNode.strip_uuid(uuid)
        return self._get_tree_queryset().get(uuid_full__startswith=uuid)

    def has_nodes_for_process(self, uuid, clean=True):
        """
        Returns if the sample has any nodes corresponding to the specified
        process.

        :param uuid: The uuid of the process to search for.
        :param clean: Whether to clean the provided uuid. Defaults to True.
        :returns: Whether the sample has any nodes with the specified process.
        """
        return self.get_nodes_for_process(uuid, clean).exists()

    def get_nodes_for_process(self, uuid, clean=True):
        """
        Get all nodes from the tree that have the specified process.

        :param uuid: The uuid of the process to search for.
        :param clean: Whether to clean the provided uuid. Defaults to True.
        :returns: The nodes for the sample with the specified process.
        """
        if clean:
            uuid = Process.strip_uuid(uuid)
        return self._get_tree_queryset().filter(process__uuid_full__startswith=uuid)

    def has_nodes_for_process_type(self, process_type):
        """
        Returns if the sample has any nodes corresponding to the specified
        process type.

        :param process_type: The process class to search for.
        :returns: Whether the sample has any nodes with the specified process
                  type.
        :raises ValueError: If the provided process type class is not a valid
                            process.
        """
        return self.get_nodes_for_process_type(process_type).exists()

    def get_nodes_for_process_type(self, process_type):
        """
        Get all nodes from the tree that have the specified process type.

        :param process_type: The process class to search for.
        :returns: The nodes for the sample with the specified process type.
        :raises ValueError: If the provided process type class is not a valid
                            process.
        """
        if process_type != Process and Process not in process_type.__bases__:
            raise ValueError('{} is not a valid process, it does not inherit '
                             'from Process'.format(process_type.__name__))
        content_type = ContentType.objects.get_for_model(process_type).id
        return self._get_tree_queryset().filter(
            process__polymorphic_ctype=content_type)
