# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from django.utils import timezone

from model_mommy import mommy

from core.models import Sample


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


class TestUIDMixin(unittest.TestCase):

    def test_set_uid(self):
        Sample.prefix = 'prefix'
        Sample.postfix = 'postfix'
        Sample.padding = 6
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create(substrate=substrate, process_tree=None)
        expected = 'prefix{0}postfix'.format(str(sample.id).zfill(6))
        self.assertEqual(expected, sample.uid)


class TestSampleManager(unittest.TestCase):

    def test_create_sample_no_process(self):
        """
        Test that the sample is properly created with a null process_tree
        when it is created without any associated process.
        """
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create_sample(substrate=substrate)
        self.assertEqual(substrate.id, sample.substrate_id)
        self.assertIsNone(sample.process_tree)

    def test_create_sample_with_process(self):
        """
        Test that the sample is properly created with a process_tree when a
        process is specified.
        """
        substrate = mommy.make('core.Substrate')
        process = mommy.make('core.Process')
        sample = Sample.objects.create_sample(substrate=substrate,
                                              process=process)
        self.assertIsNotNone(sample.process_tree)
        self.assertEqual(process.id, sample.process_tree.process_id)

    def test_create_sample_multiple_nodes_shared_process(self):
        """
        Test that multiple samples can share a process but will have different
        trees.
        """
        substrate_1 = mommy.make('core.Substrate')
        substrate_2 = mommy.make('core.Substrate')
        process = mommy.make('core.Process')
        sample_1 = Sample.objects.create_sample(substrate=substrate_1,
                                                process=process)
        sample_2 = Sample.objects.create_sample(substrate=substrate_2,
                                                process=process)
        self.assertNotEqual(sample_1.process_tree_id, sample_2.process_tree_id)
        self.assertEqual(sample_1.process_tree.process_id,
                         sample_2.process_tree.process_id)


class TestSample(unittest.TestCase):

    def test_split_sample_no_process(self):
        """
        Test that splitting a sample with no other processes done on it in half
        results in 2 child nodes.
        """
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create_sample(substrate=substrate)
        sample.split_sample(2)
        self.assertIsNotNone(sample.process_tree)
        self.assertEqual(2, sample.process_tree.get_descendant_count())

    def test_split_sample_with_process(self):
        """
        Test that splitting a sample that already has had processes done on it
        in half results in two additional nodes.
        """
        substrate = mommy.make('core.Substrate')
        process = mommy.make('core.Process', uid='proc-0001')
        sample = Sample.objects.create_sample(substrate, process=process)
        initial = sample.process_tree.get_descendant_count()
        sample.split_sample(2)
        final = sample.process_tree.get_descendant_count()
        self.assertEqual(initial + 2, final)
