# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.core.exceptions import ValidationError

from core.validators import validate_not_zero


class TestValidateNotZero(unittest.TestCase):

    def test_positive(self):
        validate_not_zero(1)

    def test_negative(self):
        with self.assertRaises(ValidationError):
            validate_not_zero(-1)

    def test_zero(self):
        with self.assertRaises(ValidationError):
            validate_not_zero(0)
