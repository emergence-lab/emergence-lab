# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.utils import timezone

from model_mommy import mommy

from core.models import Sample, Process


class TestActiveStateMixin(unittest.TestCase):

    def test_activate_valid(self):
        obj = mommy.prepare('core.Project', is_active=False)
        self.assertFalse(obj.is_active)
        obj.activate()
        self.assertTrue(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_activate_invalid(self):
        obj = mommy.prepare('core.Project', is_active=True)
        with self.assertRaises(Exception):
            obj.activate()

    def test_deactivate_valid(self):
        obj = mommy.prepare('core.Project', is_active=True)
        self.assertTrue(obj.is_active)
        obj.deactivate()
        self.assertFalse(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_deactivate_invalid(self):
        obj = mommy.prepare('core.Project', is_active=False)
        with self.assertRaises(Exception):
            obj.deactivate()


class TestUUIDMixin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Process.prefix = 'prefix'
        Process.short_length = 10

    def test_uuid_prefix(self):
        process = mommy.make(Process)
        self.assertTrue(process.uuid.startswith(Process.prefix))

    def test_strip_uuid_short(self):
        process = mommy.make(Process)
        self.assertEqual(Process.strip_uuid(process.uuid),
                         process.uuid[len(Process.prefix):])

    def test_strip_uuid_long(self):
        process = mommy.make(Process)
        self.assertEqual(Process.strip_uuid(process.uuid_full),
                         process.uuid_full.hex)

    def test_short_uuid(self):
        process = mommy.make(Process)
        self.assertEqual(len(process.uuid),
                         len(Process.prefix) + Process.short_length)
        self.assertTrue(process.uuid[len(Process.prefix)])


class TestAutoUUIDMixin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Sample.prefix = 'prefix'
        Sample.padding = 6

    def setUp(self):
        substrate = mommy.make('core.Substrate')
        self.sample = Sample.objects.create(substrate=substrate)

    def test_uuid_prefix(self):
        self.assertTrue(self.sample.uuid.startswith(Sample.prefix))

    def test_strip_uuid(self):
        uuid = Sample.strip_uuid(self.sample.uuid)
        self.assertEqual(uuid, self.sample.id)


class TestSampleManager(unittest.TestCase):

    def test_create_sample(self):
        """
        Test that the sample is properly created with the root process.
        """
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create(substrate=substrate)
        self.assertEqual(substrate.id, sample.substrate_id)


class TestSample(unittest.TestCase):

    def setUp(self):
        substrate = mommy.make('core.Substrate')
        self.sample = Sample.objects.create(substrate=substrate)

    def test_insert_node_append(self):
        """
        Test that a node is properly appended to the end of the tree.
        """
        root = self.sample.process_tree
        pieces = 'abc'
        for piece in pieces:
            process = mommy.make(Process)
            node = self.sample._insert_node(process, piece, root)
            self.assertEqual(node.parent_id, root.id)
            self.assertEqual(node.piece, piece)
            self.assertEqual(node.process_id, process.id)
            self.assertEqual(node.comment, '')
        self.sample.refresh_tree()
        self.assertEqual(len(pieces),
                         self.sample.process_tree.get_descendant_count())

    def test_get_tree_queryset_single_level(self):
        """
        Test that the queryset returns the root node for a single level tree.
        """
        node = self.sample.process_tree
        qs = self.sample._get_tree_queryset()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().uuid_full, node.uuid_full)

    def test_get_tree_queryset_multiple_levels(self):
        """
        Test that the queryset returns all nodes for a multiple level tree.
        """
        node = self.sample.process_tree
        node_uuids = [node.uuid]
        levels = 4
        for level in range(levels):
            node = self.sample._insert_node(None, 'a', node)
            node_uuids.append(node.uuid)
        qs = self.sample._get_tree_queryset()
        self.assertEqual(qs.count(), levels + 1)
        for node in qs:
            self.assertIn(node.uuid, node_uuids)

    def test_leaf_nodes_single_level(self):
        """
        Test that the correct leaf nodes are returned when they are all on the
        same level.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        for piece in pieces:
            node = self.sample._insert_node(None, piece, root)
        leaf_nodes = list(self.sample.leaf_nodes)
        self.assertEqual(len(leaf_nodes), len(pieces))
        for node in leaf_nodes:
            self.assertIn(node.piece, pieces)

    def test_leaf_nodes_multiple_levels(self):
        """
        Test that the correct leaf nodes are returned when they are on different
        levels.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        levels = [1, 2, 4, 6, 7, 6, 2]
        expected_leaf_nodes = []
        for level, piece in zip(levels, pieces):
            node = self.sample._insert_node(None, piece, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, node)
            expected_leaf_nodes.append(node)
        leaf_nodes = list(self.sample.leaf_nodes)
        self.assertEqual(len(leaf_nodes), len(pieces))
        for node in leaf_nodes:
            self.assertIn(node.piece, pieces)
            self.assertIn(node, expected_leaf_nodes)

    def test_get_node_short_uuid(self):
        """
        Test that you can retrieve individual nodes in a complex tree using the
        short uuid.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        levels = [1, 2, 4, 6, 7, 6, 2]
        node_uuids = [root.uuid]
        for level, piece in zip(levels, pieces):
            node = self.sample._insert_node(None, piece, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, node)
                node_uuids.append(node.uuid)
        for uuid in node_uuids:
            node = self.sample.get_node(uuid)
            self.assertEqual(node.uuid, uuid)

    def test_get_node_long_uuid(self):
        """
        Test that you can retrieve individual nodes in a complex tree using the
        short uuid.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        levels = [1, 2, 4, 6, 7, 6, 2]
        node_uuids = [root.uuid_full]
        for level, piece in zip(levels, pieces):
            node = self.sample._insert_node(None, piece, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, node)
                node_uuids.append(node.uuid_full)
        for uuid in node_uuids:
            node = self.sample.get_node(uuid)
            self.assertEqual(node.uuid_full, uuid)

    def test_pieces(self):
        """
        Test that the correct used pieces are returned.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        for piece in pieces:
            node = self.sample._insert_node(None, piece, root)
        self.assertListEqual(list(pieces), self.sample.pieces)

    def test_get_piece_single(self):
        """
        Test that the piece can be returned if there is only one piece.
        """
        root = self.sample.process_tree
        node = self.sample.get_piece(root.piece)
        self.assertEqual(root.uuid, node.uuid)

    def test_get_piece_multiple(self):
        """
        Test that the piece can be returned if there are multiple pieces.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        node_uuids = []
        for piece in pieces:
            node = self.sample._insert_node(None, piece, root)
            node_uuids.append(node.uuid)
        for uuid, piece in zip(node_uuids, pieces):
            node = self.sample.get_piece(piece)
            self.assertEqual(node.uuid, uuid)

    def test_node_count(self):
        root = self.sample.process_tree
        pieces = 'abcdefg'
        for piece in pieces:
            node = self.sample._insert_node(None, piece, root)
        self.sample.refresh_tree()
        self.assertEqual(self.sample.node_count, len(pieces) + 1)

    def test_run_process(self):
        """
        Test that running a process correctly appends it to the tree.
        """
        parent = self.sample.process_tree
        number_processes = 4
        for n in range(number_processes):
            process = mommy.make(Process)
            node = self.sample.run_process(process, parent.piece)
            self.assertEqual(node.parent_id, parent.id)
            self.assertEqual(node.process_id, process.id)
            self.assertEqual(node.piece, parent.piece)
            self.assertEqual(node.comment, '')
            parent = node
        self.assertEqual(number_processes,
                         self.sample.process_tree.get_descendant_count())

    def test_split_single(self):
        """
        Test that splitting a sample results in the correct number of nodes
        being created and that they have the correct parent node.
        """
        pieces = 'abcd'
        split_number = len(pieces)
        before = self.sample.node_count
        root = self.sample.root_node
        nodes = self.sample.split(split_number)
        after = self.sample.node_count
        self.assertEqual(before + split_number, after)
        self.assertEqual(split_number, len(nodes))
        for node in nodes:
            self.assertEqual(node.parent_id, root.id)
            self.assertIn(node.piece, pieces)
        self.assertSetEqual(set(nodes), set(self.sample.leaf_nodes))

    def test_split_multiple(self):
        """
        Test that splitting a sample multiple times results in correctly
        assigned parent nodes and piece identifiers.
        """
        pieces_first = 'abcd'
        pieces_second = 'befg'
        split_number = 4
        before = self.sample.node_count
        root_first = self.sample.root_node
        nodes_first = self.sample.split(split_number, 'a')
        root_second = self.sample.get_piece('b')
        nodes_second = self.sample.split(split_number, 'b')
        after = self.sample.node_count
        self.assertEqual(split_number * 2 + before, after)
        for node in nodes_first:
            self.assertEqual(node.parent_id, root_first.id)
            self.assertIn(node.piece, pieces_first)
        for node in nodes_second:
            self.assertEqual(node.parent_id, root_second.id)
            self.assertIn(node.piece, pieces_second)

    def test_insert_process_before(self):
        root = self.sample.root_node
        node_first = self.sample.run_process(None)
        node_second = self.sample.insert_process_before(None, node_first.uuid)
        node_first = self.sample.get_node(node_first.uuid)
        node_second = self.sample.get_node(node_second.uuid)
        self.assertEqual(node_second.parent_id, root.id)
        self.assertEqual(node_first.parent_id, node_second.id)
        self.assertEqual(len(self.sample.leaf_nodes), 1)
        self.assertEqual(self.sample.leaf_nodes[0].id, node_first.id)

    def test_insert_process_after(self):
        root = self.sample.root_node
        node_first = self.sample.run_process(None)
        node_second = self.sample.insert_process_after(None, root.uuid)
        node_first = self.sample.get_node(node_first.uuid)
        node_second = self.sample.get_node(node_second.uuid)
        self.assertEqual(node_second.parent_id, root.id)
        self.assertEqual(node_first.parent_id, node_second.id)
        self.assertEqual(len(self.sample.leaf_nodes), 1)
        self.assertEqual(self.sample.leaf_nodes[0].id, node_first.id)
