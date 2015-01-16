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
