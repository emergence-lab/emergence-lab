# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from model_mommy import mommy

from core.configuration.models import (
    AppConfigurationDefault,
    AppConfigurationSubscription,
    ConfigurationManager,
    get_configuration_default,
    get_configuration_choices,
    list_configuration_keys,
)

from core.configuration.tests.models import ConfigurationTestModel


class TestAppConfiguration(TestCase):

    def setUp(self):
        AppConfigurationDefault.objects.all().delete()

    def test_app_config_str(self):
        choices = ['a', 'b', 'c']
        config = mommy.make(AppConfigurationDefault, key='test_key',
                                                     default_value='a',
                                                     choices=choices)
        self.assertEqual(str(config), 'test_key: a {}'.format(choices))

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
        config = mommy.make(AppConfigurationDefault, key='test_key')
        value = get_configuration_default('test_key')
        self.assertEqual(config.default_value, '')

    def test_get_configuration_default_valid(self):
        config = mommy.make(AppConfigurationDefault, key='test_key',
                                                     default_value='value')
        value = get_configuration_default('test_key')
        self.assertEqual(config.default_value, value)

    def test_get_configuration_choices_invalid_type(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices(1)

    def test_get_configuration_choices_invalid_empty_string(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices('')

    def test_get_configuration_choices_invalid_key(self):
        with self.assertRaises(AppConfigurationDefault.DoesNotExist):
            get_configuration_choices('app_key')

    def test_get_configuration_choices_valid(self):
        config = mommy.make(AppConfigurationDefault, key='test_key',
                                                     default_value='a',
                                                     choices=['a', 'b'])
        choices = get_configuration_choices('test_key')
        self.assertEqual(config.choices, choices)

    def test_get_configuration_choices_none_defined(self):
        config = mommy.make(AppConfigurationDefault, key='test_key')
        choices = get_configuration_choices('test_key')
        self.assertEqual(config.choices, [])

    def test_list_configuration_keys_invalid_type(self):
        with self.assertRaises(TypeError):
            list_configuration_keys(1)

    def test_list_configuration_keys_invalid_empty_string(self):
        self.assertListEqual(list_configuration_keys(''), [])

    def test_list_configuration_keys_no_app(self):
        config = [
            mommy.make(AppConfigurationDefault, key='test_key1'),
            mommy.make(AppConfigurationDefault, key='test_key2'),
            mommy.make(AppConfigurationDefault, key='test_key3'),
            mommy.make(AppConfigurationDefault, key='alt_key1'),
            mommy.make(AppConfigurationDefault, key='alt_key2'),
        ]
        keys = list_configuration_keys()
        self.assertListEqual([c.key for c in config], keys)

    def test_list_configuration_keys_with_app(self):
        config = [
            mommy.make(AppConfigurationDefault, key='test_key1'),
            mommy.make(AppConfigurationDefault, key='test_key2'),
            mommy.make(AppConfigurationDefault, key='test_key3'),
            mommy.make(AppConfigurationDefault, key='alt_key1'),
            mommy.make(AppConfigurationDefault, key='alt_key2'),
        ]
        keys = list_configuration_keys('test')
        self.assertListEqual([c.key for c in config if 'test' in c.key], keys)

    def test_subscription_str(self):
        subscription = mommy.make(AppConfigurationSubscription,
            app_label='app', model_name='model')
        self.assertEqual(str(subscription), 'app.model')

    def test_subscription_manager_create_no_configuration(self):
        config = mommy.make(AppConfigurationDefault, key='test_key', default_value='value')
        test = ConfigurationTestModel.objects.create()
        self.assertEqual(test.configuration[config.key], config.default_value)

    def test_subscription_manager_create_with_configuration(self):
        config = mommy.make(AppConfigurationDefault, key='test_key', default_value='value')
        test = ConfigurationTestModel.objects.create(configuration={'test_key': 'edited'})
        self.assertEqual(test.configuration[config.key], 'edited')
