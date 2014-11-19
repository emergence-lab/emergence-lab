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


class TestSampleManager(unittest.TestCase):

    def test_create_sample_no_process(self):
        substrate = mommy.make('core.Substrate')
        sample = Sample.objects.create_sample(substrate=substrate)
        self.assertEqual(substrate.id, sample.substrate_id)
        self.assertIsNone(sample.process_tree)

    def test_create_sample_with_process(self):
        substrate = mommy.make('core.Substrate')
        process = mommy.make('core.Process')
        sample = Sample.objects.create_sample(substrate=substrate,
                                              process=process)
        self.assertIsNotNone(sample.process_tree)
        self.assertEqual(process.id, sample.process_tree.process_id)
