# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from model_mommy import mommy

from core.configuration.models import (
    AppConfigurationDefault,
    get_configuration_default,
    get_configuration_choices,
    list_configuration_keys,
)

class TestAppConfiguration(TestCase):

    def test_app_config_str(self):
        choices = ['a', 'b', 'c']
        config = mommy.make(AppConfigurationDefault, key='test.key',
                                                     default_value='a',
                                                     choices=choices)
        self.assertEqual(str(config), 'test.key: a {}'.format(choices))

    def test_get_configuration_default_invalid_type(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_default(1)

    def test_get_configuration_default_invalid_empty_string(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_default('')

    def test_get_configuration_default_invalid_key(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_default('app.key')

    def test_get_configuration_default_none_defined(self):
        config = mommy.make(AppConfigurationDefault, key='test.key')
        value = get_configuration_default('test.key')
        self.assertEqual(config.default_value, '')

    def test_get_configuration_default_valid(self):
        config = mommy.make(AppConfigurationDefault, key='test.key',
                                                     default_value='value')
        value = get_configuration_default('test.key')
        self.assertEqual(config.default_value, value)

    def test_get_configuration_choices_invalid_type(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices(1)

    def test_get_configuration_choices_invalid_empty_string(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices('')

    def test_get_configuration_choices_invalid_key(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices('app.key')

    def test_get_configuration_choices_valid(self):
        config = mommy.make(AppConfigurationDefault, key='test.key',
                                                     default_value='a',
                                                     choices=['a', 'b'])
        choices = get_configuration_choices('test.key')
        self.assertEqual(config.choices, choices)

    def test_get_configuration_choices_none_defined(self):
        config = mommy.make(AppConfigurationDefault, key='test.key')
        choices = get_configuration_choices('test.key')
        self.assertEqual(config.choices, [])

    def test_list_configuration_keys_invalid_type(self):
        with self.assertRaises(TypeError):
            list_configuration_keys(1)

    def test_list_configuration_keys_invalid_empty_string(self):
        self.assertListEqual(list_configuration_keys(''), [])

    def test_list_configuration_keys_no_app(self):
        AppConfigurationDefault.objects.all().delete()
        config = [
            mommy.make(AppConfigurationDefault, key='test.key1'),
            mommy.make(AppConfigurationDefault, key='test.key2'),
            mommy.make(AppConfigurationDefault, key='test.key3'),
            mommy.make(AppConfigurationDefault, key='alt.key1'),
            mommy.make(AppConfigurationDefault, key='alt.key2'),
        ]
        keys = list_configuration_keys()
        self.assertListEqual([c.key for c in config], keys)

    def test_list_configuration_keys_with_app(self):
        AppConfigurationDefault.objects.all().delete()
        config = [
            mommy.make(AppConfigurationDefault, key='test.key1'),
            mommy.make(AppConfigurationDefault, key='test.key2'),
            mommy.make(AppConfigurationDefault, key='test.key3'),
            mommy.make(AppConfigurationDefault, key='alt.key1'),
            mommy.make(AppConfigurationDefault, key='alt.key2'),
        ]
        keys = list_configuration_keys('test')
        self.assertListEqual([c.key for c in config if 'test' in c.key], keys)
