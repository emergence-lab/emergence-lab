# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from itertools import product
from unittest import TestCase

from afm import utils


class TestAFMUtils(TestCase):

    def test_extract_scan_number_non_integer(self):
        """Test if the extension is not convertible to an integer."""
        filename = 'file.txt'
        with self.assertRaises(ValueError):
            utils.extract_scan_number(filename)

    def test_extract_scan_number_nonpadded_integer(self):
        """Test if the extension is a non-padded integer."""
        filename = 'file.123'
        number = utils.extract_scan_number(filename)
        self.assertEqual(number, 123)

    def test_extract_scan_number_padded_integer(self):
        """Test if the extension is a zero-padded integer."""
        filename = 'file.001'
        number = utils.extract_scan_number(filename)
        self.assertEqual(number, 1)

    def test_extract_location_no_characters(self):
        """Test if the filename does not contain the split characters."""
        filename = 'test.txt'
        location = utils.extract_scan_location(filename, default_location='test')
        self.assertEqual(location, 'test')

    def test_extract_location_invalid_location(self):
        """Test if the filename contains an invalid location."""
        filename = 'test_a.txt'
        location = utils.extract_scan_location(filename, default_location='test')
        self.assertEqual(location, 'test')

    def test_extract_location_valid_location(self):
        filename = 'test{}{}.txt'
        for s, l in product('-_', 'rRcCfFeE'):
            location = utils.extract_scan_location(filename.format(s, l),
                                                   default_location='test')
            self.assertEqual(location, l)

