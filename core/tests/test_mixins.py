# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.utils import timezone

from model_mommy import mommy

from core.tests.models import ActiveStateModel, AutoUUIDModel, UUIDModel


class TestActiveStateMixin(unittest.TestCase):

    def test_activate_valid(self):
        obj = mommy.prepare(ActiveStateModel, is_active=False)
        self.assertFalse(obj.is_active)
        obj.activate()
        self.assertTrue(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_activate_invalid(self):
        obj = mommy.prepare(ActiveStateModel, is_active=True)
        with self.assertRaises(Exception):
            obj.activate()

    def test_deactivate_valid(self):
        obj = mommy.prepare(ActiveStateModel, is_active=True)
        self.assertTrue(obj.is_active)
        obj.deactivate()
        self.assertFalse(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_deactivate_invalid(self):
        obj = mommy.prepare(ActiveStateModel, is_active=False)
        with self.assertRaises(Exception):
            obj.deactivate()

    def test_manager_get_qs(self):
        active_obj = mommy.make(ActiveStateModel, is_active=True)
        inactive_obj = mommy.make(ActiveStateModel, is_active=False)
        self.assertIn(active_obj, ActiveStateModel.active.all())
        self.assertNotIn(active_obj, ActiveStateModel.inactive.all())
        self.assertIn(inactive_obj, ActiveStateModel.inactive.all())
        self.assertNotIn(inactive_obj, ActiveStateModel.active.all())


class TestUUIDMixin(unittest.TestCase):

    def setUp(self):
        self.obj = mommy.make(UUIDModel)

    def test_uuid_prefix(self):
        self.assertTrue(self.obj.uuid.startswith(UUIDModel.prefix))

    def test_strip_uuid_short(self):
        self.assertEqual(UUIDModel.strip_uuid(self.obj.uuid),
                         self.obj.uuid[len(UUIDModel.prefix):])

    def test_strip_uuid_long(self):
        self.assertEqual(UUIDModel.strip_uuid(self.obj.uuid_full),
                         self.obj.uuid_full.hex)

    def test_strip_uuid_long_string(self):
        self.assertEqual(UUIDModel.strip_uuid(self.obj.uuid_full.hex),
                         self.obj.uuid_full.hex)

    def test_short_uuid(self):
        self.assertEqual(len(self.obj.uuid),
                         len(UUIDModel.prefix) + UUIDModel.short_length)
        self.assertTrue(self.obj.uuid[len(UUIDModel.prefix)])


class TestAutoUUIDMixin(unittest.TestCase):

    def setUp(self):
        self.obj = mommy.make(AutoUUIDModel)

    def test_uuid_prefix(self):
        self.assertTrue(self.obj.uuid.startswith(AutoUUIDModel.prefix))

    def test_strip_uuid(self):
        uuid = AutoUUIDModel.strip_uuid(self.obj.uuid)
        self.assertEqual(uuid, self.obj.id)
