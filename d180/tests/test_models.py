# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from core.models import SampleNode
from d180.models import Growth


class TestGrowth(TestCase):

    def test_growth_str(self):
        growth_number = 'g1000'
        obj = mommy.prepare(Growth, uid=growth_number)
        self.assertEqual(obj.__str__(), growth_number)

    def test_get_growth_invalid(self):
        with self.assertRaisesRegexp(Exception, 'improperly formatted'):
            Growth.get_growth('xxxx')

    def test_get_growth_does_not_exist(self):
        with self.assertRaisesRegexp(Exception, 'does not exist'):
            Growth.get_growth('g1000')

    def test_get_growth_single_returned(self):
        growth_number = 'g1000'
        obj = mommy.make(Growth, uid=growth_number)
        self.assertEqual(obj, Growth.get_growth(growth_number))
