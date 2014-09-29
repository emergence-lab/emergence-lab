# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import platter


class TestPlatter(TestCase):

    def test_activate_valid(self):
        obj = platter(name='platter 1', active=False,
                     start_date=timezone.now() - timedelta(days=30),
                     end_date=timezone.now())
        self.assertFalse(obj.active)
        obj.activate()
        self.assertTrue(obj.active)

    def test_activate_invalid(self):
        obj = platter(name='platter 1', active=True,
                     start_date=timezone.now() - timedelta(days=30))
        with self.assertRaises(Exception):
            obj.activate()

    def test_deactivate_valid(self):
        obj = platter(name='platter 1', active=True,
                     start_date=timezone.now() - timedelta(days=30))
        self.assertTrue(obj.active)
        obj.deactivate()
        self.assertFalse(obj.active)
        self.assertEqual(timezone.now().date(), obj.end_date.date())

    def test_deactivate_invalid(self):
        obj = platter(name='platter 1', active=False,
                     start_date=timezone.now() - timedelta(days=30),
                     end_date=timezone.now())
        with self.assertRaises(Exception):
            obj.deactivate()
