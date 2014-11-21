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

    @classmethod
    def setUpClass(cls):
        Sample.prefix = 'prefix'
        Sample.postfix = 'postfix'
        Sample.padding = 6

    def setUp(self):
        self.substrate = mommy.make('core.Substrate')

    def test_auto_both(self):
        sample = Sample.objects.create(substrate=self.substrate,
                                       process_tree=None)
        expected = 'prefix{0}postfix'.format(str(sample.id).zfill(6))
        self.assertEqual(expected, sample.uid)

    def test_set_id_auto_uid(self):
        sample = Sample.objects.create(id=1000, substrate=self.substrate,
                                       process_tree=None)
        expected = 'prefix001000postfix'
        self.assertEqual(expected, sample.uid)

    def test_set_prefix(self):
        sample = Sample.objects.create(uid='new-{id}{postfix}',
                                       substrate=self.substrate,
                                       process_tree=None)
        expected = 'new-{0}postfix'.format(str(sample.id).zfill(6))
        self.assertEqual(expected, sample.uid)

    def test_set_postfix(self):
        sample = Sample.objects.create(uid='{prefix}{id}-new',
                                       substrate=self.substrate,
                                       process_tree=None)
        expected = 'prefix{0}-new'.format(str(sample.id).zfill(6))
        self.assertEqual(expected, sample.uid)


class TestSampleManager(unittest.TestCase):

    def test_create_sample(self):
        """
        Test that the sample is properly created with the root process.
        """
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create_sample(substrate=substrate)
        self.assertEqual(substrate.id, sample.substrate_id)
        self.assertEqual(sample.uid + '_a.root', sample.process_tree.uid)


class TestSample(unittest.TestCase):

    def setUp(self):
        self.substrate = mommy.make('core.Substrate')

    def test_split_sample(self):
        """
        Test that splitting a sample with no other processes done on it in half
        results in 2 child nodes.
        """
        split_number = 4
        sample = Sample.objects.create_sample(substrate=self.substrate)
        before = sample.process_tree.get_descendant_count()
        sample.split(split_number)
        after = sample.process_tree.get_descendant_count()
        self.assertEqual(before + split_number, after)

    def test_multiple_split_sample(self):
        """
        Test that splitting a sample multiple times correctly assigns piece
        letters
        """
        sample = Sample.objects.create_sample(substrate=self.substrate)
        self.assertEqual(sample.process_tree.piece, 'a')
        sample.split(2, 'a')
        before_a = sample.get_piece('a')
        before_b = sample.get_piece('b')
        before_c = sample.get_piece('c')
        self.assertIsNotNone(before_a)
        self.assertIsNotNone(before_b)
        self.assertIsNone(before_c)
        sample.split(2, 'b')
        after_a = sample.get_piece('a')
        after_b = sample.get_piece('b')
        after_c = sample.get_piece('c')
        self.assertEqual(before_a.id, after_a.id)
        self.assertNotEqual(before_b.id, after_b.id)
        self.assertIsNotNone(after_c)
        self.assertEqual(after_b.parent_id, before_b.id)
        self.assertEqual(after_c.parent_id, before_b.id)

    def test_get_piece(self):
        sample = Sample.objects.create_sample(self.substrate)
        sample.split(2)
        left = sample.get_piece('a')
        right = sample.get_piece('b')
        self.assertEqual(left.piece, 'a')
        self.assertEqual(right.piece, 'b')
        self.assertEqual(left.parent, sample.process_tree)
        self.assertEqual(right.parent, sample.process_tree)


    def test_get_process_single(self):
        sample = Sample.objects.create_sample(self.substrate)
        process = sample.process_tree.process
        result = sample.get_process(process.uid)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().id, sample.process_tree.id)
