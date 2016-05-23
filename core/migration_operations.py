# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import router
from django.db.migrations.operations.base import Operation


class PublishAppConfiguration(Operation):
    reversible = False
    reduces_to_sql = False
    atomic = False
    elidable = False

    def __init__(self, key, default_value=None, choices=None):
        self.key = key
        self.default_value = default_value
        self.choices = choices

    def deconstruct(self):
        return (
            self.__class__.__name__,
            [],
            {
                'key': self.key,
                'default_value': self.default_value,
                'choices': self.choices,
            }
        )

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            full_key = '{}.{}'.format(app_label, self.key)
            AppConfigurationDefault = from_state.apps.get_model('core', 'AppConfigurationDefault')
            config, _ = AppConfigurationDefault.objects.get_or_create(key=full_key)
            if self.default_value is not None:
                config.default_value = self.default_value
            if self.choices is not None:
                config.choices = self.choices
            config.save()

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        raise NotImplementedError('You cannot reverse this operation')

    def describe(self):
        return 'Creates or updates the default configuration value for an application.'
