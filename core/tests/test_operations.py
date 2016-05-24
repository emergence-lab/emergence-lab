# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.apps.registry import Apps
from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TestCase

from core.migration_operations import PublishAppConfiguration
from core.models import AppConfigurationDefault


class TestAppConfigurationMigrationOperations(TestCase):

    def _migrate(self, migration):
        old_state = ProjectState(real_apps=['core'])
        new_state = old_state.clone()
        with connection.schema_editor() as editor:
            migration.database_forwards('test', editor, old_state, new_state)
        return AppConfigurationDefault.objects.last()

    def test_publish_invalid_key_type(self):
        with self.assertRaises(TypeError):
            PublishAppConfiguration(key=None)

    def test_publish_invalid_empty_key(self):
        with self.assertRaises(ValueError):
            PublishAppConfiguration(key='')

    def test_publish_invalid_key_with_dot(self):
        with self.assertRaises(ValueError):
            PublishAppConfiguration(key='test.key')

    def test_publish_invalid_value_type(self):
        with self.assertRaises(TypeError):
            PublishAppConfiguration(key='test', default_value=1)

    def test_publish_invalid_choices_type(self):
        with self.assertRaises(TypeError):
            PublishAppConfiguration(key='test', choices='single_choice')

    def test_publish_invalid_choices_subtype(self):
        with self.assertRaises(TypeError):
            PublishAppConfiguration(key='test', choices=[1, 2])

    def test_publish_invalid_default_is_not_choice(self):
        with self.assertRaises(ValueError):
            PublishAppConfiguration(key='test', default_value='test',
                                    choices=['single_choice'])

    def test_publish_valid_empty_args(self):
        migration = PublishAppConfiguration(key='test')
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test.test')
        self.assertEqual(config.default_value, '')
        self.assertEqual(config.choices, [])

    def test_publish_valid_empty_choices(self):
        migration = PublishAppConfiguration(key='test', default_value='value')
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test.test')
        self.assertEqual(config.default_value, 'value')
        self.assertEqual(config.choices, [])

    def test_publish_valid(self):
        migration = PublishAppConfiguration(key='test', default_value='value',
                                            choices=['value', 'alternate'])
        config = self._migrate(migration)
        self.assertEqual(config.key, 'test.test')
        self.assertEqual(config.default_value, 'value')
        self.assertEqual(config.choices, ['value', 'alternate'])
