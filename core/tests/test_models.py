# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from django.utils import timezone

from model_mommy import mommy

from core.models import platter


class TestPlatter(unittest.TestCase):

    def test_activate_valid(self):
        obj = mommy.prepare(platter, is_active=False)
        self.assertFalse(obj.is_active)
        obj.activate()
        self.assertTrue(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_activate_invalid(self):
        obj = mommy.prepare(platter, is_active=True)
        with self.assertRaises(Exception):
            obj.activate()

    def test_deactivate_valid(self):
        obj = mommy.prepare(platter, is_active=True)
        self.assertTrue(obj.is_active)
        obj.deactivate()
        self.assertFalse(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_deactivate_invalid(self):
        obj = mommy.prepare(platter, is_active=False)
        with self.assertRaises(Exception):
            obj.deactivate()
