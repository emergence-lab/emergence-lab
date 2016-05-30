# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.apps.registry import Apps
from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TestCase

import six

from core.configuration.operations import PublishConfiguration
from core.configuration.models import AppConfigurationDefault


class TestAppConfigurationMigrationOperations(TestCase):

    def _migrate(self, migration):
        old_state = ProjectState(real_apps=['configuration', 'core'])
        new_state = old_state.clone()
        with connection.schema_editor() as editor:
            migration.database_forwards('test', editor, old_state, new_state)
        return AppConfigurationDefault.objects.last()

    def test_publish_invalid_key_type(self):
        with self.assertRaises(TypeError):
            PublishConfiguration(key=None)

    def test_publish_invalid_empty_key(self):
        with self.assertRaises(ValueError):
            PublishConfiguration(key='')

    def test_publish_invalid_key_with_dot(self):
        with self.assertRaises(ValueError):
            PublishConfiguration(key='test.key')

    def test_publish_invalid_value_type(self):
        with self.assertRaises(TypeError):
            PublishConfiguration(key='test', default_value={'a': (2, 3)})

    def test_publish_invalid_choices_type_iterable(self):
        with self.assertRaises(TypeError):
            PublishConfiguration(key='test', choices='single_choice')

    def test_publish_invalid_choices_type_noniterable(self):
        with self.assertRaises(TypeError):
            PublishConfiguration(key='test', choices=123)

    def test_publish_invalid_choices_subtype(self):
        with self.assertRaises(TypeError):
            PublishConfiguration(key='test', choices=[{'a': 'b'}, 2, ('a', 1)])


    def test_publish_invalid_default_is_not_choice(self):
        with self.assertRaises(ValueError):
            PublishConfiguration(key='test', default_value='test',
                                    choices=['single_choice'])

    def test_publish_valid_empty_args(self):
        migration = PublishConfiguration(key='test')
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test_test')
        self.assertEqual(config.default_value, '')
        self.assertEqual(config.choices, [])

    def test_publish_valid_empty_choices(self):
        migration = PublishConfiguration(key='test', default_value='value')
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test_test')
        self.assertEqual(config.default_value, 'value')
        self.assertEqual(config.choices, [])

    def test_publish_valid(self):
        migration = PublishConfiguration(key='test', default_value='value',
                                            choices=['value', 'alternate'])
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test_test')
        self.assertEqual(config.default_value, 'value')
        self.assertEqual(config.choices, ['value', 'alternate'])

    def test_deconstruct(self):
        kwargs = {
            'key': 'test',
            'default_value': 'value',
            'choices': ['value', 'alternative'],
        }
        migration = PublishConfiguration(**kwargs)
        result = migration.deconstruct()
        self.assertEqual(result[0], 'PublishConfiguration')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], kwargs)

    def test_database_backwards(self):
        migration = PublishConfiguration(key='test')
        old_state = ProjectState(real_apps=['core'])
        new_state = old_state.clone()
        with connection.schema_editor() as editor:
            with self.assertRaises(NotImplementedError):
                migration.database_backwards('test', editor, old_state, new_state)

    def test_describe(self):
        migration = PublishConfiguration(key='test')
        self.assertIsInstance(migration.describe(), six.string_types)
