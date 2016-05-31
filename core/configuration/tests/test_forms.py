# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from model_mommy import mommy

from core.configuration.tests.models import ConfigurationTestModel
from core.configuration.models import AppConfigurationDefault
from core.configuration.forms import ConfigurationChoiceField


class TestConfigurationChoiceField(TestCase):

    def test_init_key_with_choices(self):
        choices = ['default', 'option1', 'option2']
        mommy.make(AppConfigurationDefault,
                   key='configuration_tests_choices_key',
                   default_value=choices[0],
                   choices=choices)
        field = ConfigurationChoiceField(key='configuration_tests_choices_key')
        field_choices = [(c, c.title()) for c in choices]
        self.assertListEqual(list(field.choices), field_choices)

    def test_init_key_without_choices(self):
        with self.assertRaises(ValueError):
            field = ConfigurationChoiceField(key='configuration_tests_existing_key')
            list(field.choices)
