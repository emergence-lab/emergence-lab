# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import platter


class TestPlatter(TestCase):

    def test_activate_valid(self):
        obj = platter(name='platter 1', is_active=False,
                     start_date=timezone.now() - timedelta(days=30),
                     status_changed=timezone.now())
        self.assertFalse(obj.is_active)
        obj.activate()
        self.assertTrue(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_activate_invalid(self):
        obj = platter(name='platter 1', is_active=True,
                     start_date=timezone.now() - timedelta(days=30))
        with self.assertRaises(Exception):
            obj.activate()

    def test_deactivate_valid(self):
        obj = platter(name='platter 1', is_active=True,
                     start_date=timezone.now() - timedelta(days=30))
        self.assertTrue(obj.is_active)
        self.assertEqual(obj.status_changed, None)
        obj.deactivate()
        self.assertFalse(obj.is_active)
        self.assertEqual(obj.status_changed.date(), timezone.now().date())

    def test_deactivate_invalid(self):
        obj = platter(name='platter 1', is_active=False,
                     start_date=timezone.now() - timedelta(days=30),
                     status_changed=timezone.now())
        with self.assertRaises(Exception):
            obj.deactivate()
