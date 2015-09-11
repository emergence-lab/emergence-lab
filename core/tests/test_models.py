# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from core.models import Sample, Process, Project


class TestSampleManager(TestCase):

    def test_create_sample(self):
        """
        Test that the sample is properly created with the root process.
        """
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create(substrate=substrate)
        self.assertEqual(substrate.id, sample.substrate_id)

    def test_get_by_uuid_nonexistant(self):
        with self.assertRaises(ObjectDoesNotExist):
            Sample.objects.get_by_uuid('s0000')

    def test_get_by_uuid_short(self):
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create(substrate=substrate)
        result = Sample.objects.get_by_uuid(sample.uuid)
        self.assertEqual(sample.uuid, result.uuid)

    def test_get_by_uuid_long(self):
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create(substrate=substrate)
        result = Sample.objects.get_by_uuid(sample.uuid_full)
        self.assertEqual(sample.uuid, result.uuid)

    def test_by_process_nonexistant(self):
        process_uuid = Process.prefix + ''.zfill(Process.short_length)
        samples = Sample.objects.by_process(process_uuid)
        self.assertQuerysetEqual(samples, [])

    def test_by_process_no_samples(self):
        process = mommy.make(Process)
        samples = Sample.objects.by_process(process.uuid)
        self.assertQuerysetEqual(samples, [])

    def test_by_process_multiple(self):
        process = mommy.make(Process)
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        for sample in samples:
            sample.run_process(process)
        extra_process = mommy.make(Process)
        extra_sample = Sample.objects.create(
            substrate=mommy.make('core.Substrate'))
        extra_sample.run_process(extra_process)
        results = Sample.objects.by_process(process.uuid)
        for sample in samples:
            self.assertIn(sample, results)
        self.assertNotIn(extra_sample, results)

    def test_by_process_type_invalid(self):
        with self.assertRaises(ValueError):
            Sample.objects.by_process_type('nonexistant')

    def test_by_process_type_no_samples(self):
        samples = Sample.objects.by_process_type('generic-process')
        self.assertQuerysetEqual(samples, [])

    def test_by_process_type_multiple(self):
        processes = [
            mommy.make(Process, type_id='generic-process'),
            mommy.make(Process, type_id='generic-process'),
            mommy.make(Process, type_id='split-process'),
        ]
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        for p, s in zip(processes, samples):
            s.run_process(p)

        process_samples = Sample.objects.by_process_type('generic-process')
        self.assertListEqual(list(process_samples), samples[:-1])
        split_samples = Sample.objects.by_process_type('split-process')
        self.assertEqual(split_samples.first(), samples[-1])

    def test_by_process_types_invalid(self):
        with self.assertRaises(ValueError):
            Sample.objects.by_process_types(['generic-process', 'nonexistant'])

    def test_by_process_types_no_samples(self):
        samples = Sample.objects.by_process_types(['generic-process',
                                                   'split-process'])
        self.assertQuerysetEqual(samples, [])

    def test_by_process_types_valid(self):
        process = mommy.make(Process, type_id='generic-process')
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        user = get_user_model().objects.create_user('default', password='')

        # run processes
        # sample 0 has only generic-process
        # sample 1 has only split-process
        # sample 2 has both generic-process and split-process
        # sample 3 has no processes
        samples[0].run_process(process)
        samples[1].split(user=user, number=2)
        samples[2].run_process(process)
        samples[2].split(user=user, number=2)

        qs = Sample.objects.by_process_types(['generic-process'], combine_and=True)
        self.assertQuerysetEqual(
            qs, map(repr, [samples[0], samples[2]]),ordered=False)
        qs = Sample.objects.by_process_types(['split-process'], combine_and=True)
        self.assertQuerysetEqual(
            qs, map(repr, samples[1:3]), ordered=False)
        qs = Sample.objects.by_process_types(['generic-process', 'split-process'], combine_and=True)
        self.assertQuerysetEqual(
            qs, map(repr, [samples[2]]), ordered=False)
        qs = Sample.objects.by_process_types(['generic-process', 'split-process'], combine_and=False)
        self.assertQuerysetEqual(
            qs, map(repr, samples[0:3]), ordered=False)


class TestSample(TestCase):

    def setUp(self):
        substrate = mommy.make('core.Substrate')
        self.sample = Sample.objects.create(substrate=substrate)
        self.user = get_user_model().objects.create_user('default', password='')

    def test_insert_node_append(self):
        """
        Test that a node is properly appended to the end of the tree.
        """
        root = self.sample.process_tree
        pieces = 'abc'
        number = 1
        for piece in pieces:
            process = mommy.make(Process)
            node = self.sample._insert_node(process, piece, number, root)
            self.assertEqual(node.parent_id, root.id)
            self.assertEqual(node.piece, piece)
            self.assertEqual(node.number, number)
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
            node = self.sample._insert_node(None, 'a', 1, node)
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
            node = self.sample._insert_node(None, piece, 1, root)
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
            node = self.sample._insert_node(None, piece, 1, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, 1, node)
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
            node = self.sample._insert_node(None, piece, 1, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, 1, node)
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
            node = self.sample._insert_node(None, piece, 1, root)
            for l in range(level):
                node = self.sample._insert_node(None, piece, 1, node)
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
            node = self.sample._insert_node(None, piece, 1, root)
        self.assertListEqual(list(pieces), list(self.sample.pieces))

    def test_get_piece_single(self):
        """
        Test that the piece can be returned if there is only one piece.
        """
        root = self.sample.process_tree
        node = self.sample.get_piece(root.piece, full=False)
        self.assertEqual(root.uuid, node.uuid)

    def test_get_piece_multiple(self):
        """
        Test that the piece can be returned if there are multiple pieces.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        node_uuids = []
        for piece in pieces:
            node = self.sample._insert_node(None, piece, 1, root)
            node_uuids.append(node.uuid)
        for uuid, piece in zip(node_uuids, pieces):
            node = self.sample.get_piece(piece, full=False)
            self.assertEqual(node.uuid, uuid)

    def test_get_piece_single_full(self):
        """
        Test that the piece can be returned if there is only one piece.
        """
        root = self.sample.process_tree
        node = self.sample.run_process(mommy.make(Process))
        nodes = self.sample.get_piece(root.piece, full=True)
        self.assertListEqual([root, node], list(nodes))

    def test_get_piece_multiple_full(self):
        """
        Test that the piece can be returned if there are multiple pieces.
        """
        root = self.sample.process_tree
        pieces = 'abcdefg'
        nodes = []
        for piece in pieces:
            node = self.sample._insert_node(None, piece, 1, root)
            nodes.append(node)
        for node, piece in zip(nodes, pieces):
            piece_nodes = self.sample.get_piece(piece, full=True)
            self.assertListEqual([root, node], list(piece_nodes))

    def test_node_count(self):
        root = self.sample.process_tree
        pieces = 'abcdefg'
        for piece in pieces:
            node = self.sample._insert_node(None, piece, 1, root)
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
        nodes = self.sample.split(self.user, split_number)
        after = self.sample.node_count
        self.assertEqual(before + split_number, after)
        self.assertEqual(split_number, len(nodes))
        for number, node in enumerate(nodes):
            self.assertEqual(node.parent_id, root.id)
            self.assertEqual(node.number, number + 1)
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
        nodes_first = self.sample.split(self.user, split_number, 'a')
        root_second = self.sample.get_piece('b')
        nodes_second = self.sample.split(self.user, split_number, 'b')
        after = self.sample.node_count
        self.assertEqual(split_number * 2 + before, after)
        for number, node in enumerate(nodes_first):
            self.assertEqual(node.parent_id, root_first.id)
            self.assertEqual(node.number, number + 1)
            self.assertIn(node.piece, pieces_first)
        for number, node in enumerate(nodes_second):
            self.assertEqual(node.parent_id, root_second.id)
            self.assertEqual(node.number, number + 1)
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

    def test_get_nodes_for_process_invalid(self):
        process_uuid = Process.prefix + ''.zfill(Process.short_length)
        results = list(self.sample.get_nodes_for_process(process_uuid))
        self.assertListEqual(results, [])

    def test_get_nodes_for_process_valid(self):
        process_1 = mommy.make(Process)
        process_2 = mommy.make(Process)
        self.sample.run_process(process_1)
        self.sample.run_process(process_2)
        results = list(self.sample.get_nodes_for_process(process_1.uuid))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].process, process_1)

    def test_has_nodes_for_process_invalid(self):
        process_uuid = Process.prefix + ''.zfill(Process.short_length)
        result = self.sample.has_nodes_for_process(process_uuid)
        self.assertFalse(result)

    def test_has_nodes_for_process_valid(self):
        process_1 = mommy.make(Process)
        self.sample.run_process(process_1)
        result = self.sample.has_nodes_for_process(process_1.uuid)
        self.assertTrue(result)

    def test_get_nodes_for_process_type_invalid(self):
        self.assertListEqual(
            [], list(self.sample.get_nodes_for_process_type('generic-process')))
        with self.assertRaises(ValueError):
            self.sample.get_nodes_for_process_type('nonexistant')

    def test_get_nodes_for_process_type_valid(self):
        process_1 = mommy.make(Process, type_id='generic-process')
        self.sample.run_process(process_1)
        p1_node = list(self.sample.leaf_nodes)
        process_2 = self.sample.split(self.user, 2)[0].process
        p2_nodes = list(self.sample.leaf_nodes)
        self.assertListEqual(
            p1_node, list(self.sample.get_nodes_for_process_type('generic-process')))
        self.assertListEqual(
            p2_nodes, list(self.sample.get_nodes_for_process_type('split-process')))

    def test_has_nodes_for_process_type_invalid(self):
        self.assertFalse(self.sample.has_nodes_for_process_type('generic-process'))
        with self.assertRaises(ValueError):
            self.sample.get_nodes_for_process_type('nonexistant')

    def test_has_nodes_for_process_type_valid(self):
        self.sample.run_process(mommy.make(Process, type_id='generic-process'))
        self.assertFalse(self.sample.has_nodes_for_process_type('split-process'))
        self.sample.split(self.user, 2)
        self.assertTrue(self.sample.has_nodes_for_process_type('generic-process'))
        self.assertTrue(self.sample.has_nodes_for_process_type('split-process'))


class TestProcess(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('default', password='')

    def test_get_samples_no_repeat(self):
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        process = Process.objects.create(comment='test', user=self.user)
        for s in samples[:-1]:
            s.run_process(process)
        sample_list = process.samples
        self.assertListEqual(list(sample_list), samples[:-1])

    def test_get_samples_with_repeat(self):
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        process = Process.objects.create(comment='test', user=self.user)
        for s in samples[:-1]:
            s.run_process(process)
        samples[0].run_process(process) # run process twice so it repeats
        sample_list = process.samples
        self.assertListEqual(list(sample_list), samples[:-1])

    def test_get_nodes(self):
        samples = [
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
            Sample.objects.create(substrate=mommy.make('core.Substrate')),
        ]
        process = Process.objects.create(comment='test', user=self.user)
        nodes = [s.run_process(process) for s in samples]
        self.assertListEqual(list(process.nodes), nodes)


class TestProject(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('default', password='')
        self.project = Project.objects.create(name='Test Project')

    def test_add_user(self):
        self.project.add_user(self.user, 'owner')
        self.assertEquals(self.project.get_membership(self.user), 'owner')
        self.assertTrue(self.project.is_viewer(self.user))
        self.assertIn(self.project.owner_group, self.user.groups.all())

    def test_remove_user(self):
        self.project.add_user(self.user, 'owner')
        self.assertEquals(self.project.get_membership(self.user), 'owner')
        self.project.remove_user(self.user)
        self.assertFalse(self.project.get_membership(self.user))

    def test_membership_inheritance(self):
        self.project.add_user(self.user, 'owner')
        self.assertTrue(self.project.is_member(self.user))

    def test_membership_heirarchy(self):
        self.project.add_user(self.user, 'viewer')
        self.assertFalse(self.project.is_owner(self.user))
