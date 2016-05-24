# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.db import router
from django.db.migrations.operations.base import Operation

import six


class PublishAppConfiguration(Operation):
    reversible = False
    reduces_to_sql = False
    atomic = False
    elidable = False

    def __init__(self, key, default_value=None, choices=None):
        if not isinstance(key, six.string_types):
            raise TypeError('key must be a string')
        if re.match(r'^((?![\.\\])[\w\d\-])+$', key) is None:
            raise ValueError('invalid key "{}"'.format(key))

        if default_value is not None:
            if not isinstance(default_value, six.string_types):
                raise TypeError('default_value must be a string')

        if choices is not None:
            if not isinstance(choices, (list, tuple)):
                raise TypeError('choices must be a list or tuple')
            for c in choices:
                if not isinstance(c, six.string_types):
                    raise TypeError('choices must be strings'.format(c))

        if choices is not None and default_value is not None:
            if default_value not in choices:
                raise ValueError('default_value must be a valid choice')

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
            default_config_model = from_state.apps.get_model('core', 'AppConfigurationDefault')
            config, _ = default_config_model.objects.get_or_create(key=full_key)
            if self.default_value is not None:
                config.default_value = self.default_value
            if self.choices is not None:
                config.choices = self.choices
            config.save()

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        raise NotImplementedError('You cannot reverse this operation')

    def describe(self):
        return 'Creates or updates the default configuration value for an application.'
