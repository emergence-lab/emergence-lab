# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from growths.models import growth, sample


class TestGrowth(TestCase):

    def test_growth_str(self):
        growth_number = 'g1000'
        obj = mommy.prepare(growth, growth_number=growth_number)
        self.assertEqual(obj.__str__(), growth_number)

    def test_get_growth_invalid(self):
        with self.assertRaisesRegexp(Exception, 'improperly formatted'):
            growth.get_growth('xxxx')

    def test_get_growth_does_not_exist(self):
        with self.assertRaisesRegexp(Exception, 'does not exist'):
            growth.get_growth('g1000')

    def test_get_growth_single_returned(self):
        growth_number = 'g1000'
        obj = mommy.make(growth, growth_number=growth_number)
        self.assertEqual(obj, growth.get_growth(growth_number))


class TestSample(TestCase):

    def test_sample_str(self):
        growth_number = 'g1000'
        growth_obj = mommy.make(growth, growth_number=growth_number)
        obj = mommy.prepare(sample, growth=growth_obj, pocket=1, piece='a')
        self.assertEqual(obj.__str__(), 'g1000_1a')

    def test_get_sample_invalid(self):
        with self.assertRaisesRegexp(Exception, 'improperly formatted'):
            sample.get_sample('xxxx')

    def test_get_sample_does_not_exist(self):
        growth_number = 'g1000'
        mommy.make(growth, growth_number=growth_number)
        with self.assertRaisesRegexp(Exception, 'Sample .+ does not exist'):
            sample.get_sample(growth_number)

    def test_get_sample_single_returned(self):
        growth_number = 'g1000'
        growth_obj = mommy.make(growth, growth_number=growth_number)
        obj = mommy.make(sample, growth=growth_obj, pocket=1)
        self.assertEqual(obj, sample.get_sample(growth_number))
        self.assertEqual(obj, sample.get_sample(growth_number + '_1'))

    def test_get_sample_multiple_returned(self):
        growth_number = 'g1000'
        growth_obj = mommy.make(growth, growth_number=growth_number)
        sample_1 = mommy.make(sample, growth=growth_obj, pocket=1)
        mommy.make(sample, growth=growth_obj, pocket=2)
        with self.assertRaisesRegexp(Exception, 'ambiguous'):
            sample.get_sample(growth_number)
        self.assertEqual(sample_1, sample.get_sample(growth_number + '_1'))

    def test_get_sample_does_match_growth(self):
        growth_number = 'g1000'
        growth_obj = mommy.make(growth, growth_number=growth_number)
        obj = mommy.make(sample, growth=growth_obj, pocket=1)
        self.assertEqual(obj, sample.get_sample(growth_number, growth_obj))

    def test_get_sample_does_not_match_growth(self):
        growth_number = 'g1000'
        growth_1 = mommy.make(growth, growth_number=growth_number)
        growth_2 = mommy.make(growth, growth_number='g1001')
        mommy.prepare(sample, growth=growth_1, pocket=1)
        with self.assertRaisesRegexp(Exception, 'does not match'):
            sample.get_sample(growth_number, growth_2)

    def test_get_sample_piece(self):
        growth_number = 'g1000'
        growth_1 = mommy.make(growth, growth_number=growth_number)
        obj = mommy.make(sample, growth=growth_1, pocket=1, piece='a')
        mommy.make(sample, growth=growth_1, pocket=1, piece='b')
        self.assertEqual(obj, sample.get_sample(growth_number + '_1a'))

    def test_get_siblings(self):
        growth_obj = mommy.make(growth, growth_number='g1000')
        samples = []
        for pocket in range(1, 7):
            samples.append(mommy.make(sample, growth=growth_obj, pocket=pocket))
        sample_obj = samples.pop()
        self.assertItemsEqual(samples, sample.get_siblings(sample_obj))

    def test_get_children(self):
        growth_1 = mommy.make(growth, growth_number='g1000')
        growth_2 = mommy.make(growth, growth_number='g1001')
        parent_sample = mommy.make(sample, growth=growth_1)
        samples = []
        for pocket in range(1, 7):
            samples.append(mommy.make(sample, growth=growth_2, pocket=pocket,
                                      parent=parent_sample))
        self.assertItemsEqual(samples, sample.get_children(parent_sample))

    def test_get_piece_siblings(self):
        growth_obj = mommy.make(growth, growth_number='g1000')
        samples = []
        for piece in 'abcdefg':
            samples.append(mommy.make(sample, growth=growth_obj,
                                      pocket=1, piece=piece))
        sample_obj = samples.pop()
        self.assertItemsEqual(samples, sample.get_piece_siblings(sample_obj))

    def test_split_first(self):
        growth_obj = mommy.make(growth, growth_number='g1000')
        sample_obj = mommy.make(sample, growth=growth_obj, pocket=1, piece='')
        sample_obj.parent = sample_obj
        pk = sample_obj.id

        samples = sample_obj.split(3)
        sample_obj = sample.objects.get(id=pk)
        self.assertEqual(sample_obj.piece, 'a')
        self.assertEqual(len(samples), 3)
        for s in samples:
            self.assertIn(s.piece, 'abc')

    def test_split_middle_piece(self):
        growth_obj = mommy.make(growth, growth_number='g1000')
        for piece in 'abc':
            sample_obj = mommy.make(sample, growth=growth_obj, pocket=1,
                                    piece=piece)
        mommy.make(sample, growth=growth_obj, pocket=1, piece='d')
        samples = sample_obj.split(3)
        for s in samples:
            self.assertIn(s.piece, 'cef')

    def test_split_last_piece(self):
        growth_obj = mommy.make(growth, growth_number='g1000')
        for piece in 'abcd':
            sample_obj = mommy.make(sample, growth=growth_obj, pocket=1,
                                    piece=piece)
        samples = sample_obj.split(3)
        for s in samples:
            self.assertIn(s.piece, 'def')
