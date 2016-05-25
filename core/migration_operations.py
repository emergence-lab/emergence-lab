# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.db import router
from django.db.migrations.operations.base import Operation

import six


class PublishAppConfiguration(Operation):

    """Migration to publish configuration key for an application.

    Creates a AppConfigurationDefault object. Configuration keys once published
    can be accessed anywhere and can be overridden on a per-instance basis
    via InstanceConfiguration.
    """

    reversible = False
    reduces_to_sql = False
    atomic = False
    elidable = False

    def __init__(self, key, default_value=None, choices=None):
        """Create app configuration object.

        :param key: The name of the configuration key - must be a string that
                    does not contain a '.' character
        :param default_value: Optional. The default value for the key. Defaults
                              to empty string if parameter is None.
        :param choices: Optional. The possible valid choices for values. Defaults
                        to empty list if parameter is None, which means any value
                        is valid.
        :raises TypeError: If the key is not a string type
        :raises ValueError: If the key is an empty string or contains a '.'
        :raises TypeError: If the default_value is not a string type or None
        :raises TypeError: If choices is not a list, tuple, or None
        :raises TypeError: If the items in choices are not strings
        :raises ValueError: If default_value is not a valid choice
        """
        self._check_init_args(key, default_value, choices)

        self.key = key
        self.default_value = default_value
        self.choices = choices

    def _check_init_args(self, key, default_value, choices):
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
            for choice in choices:
                if not isinstance(choice, six.string_types):
                    raise TypeError('choices must be strings')

        if choices is not None and default_value is not None:
            if default_value not in choices:
                raise ValueError('default_value must be a valid choice')

    def deconstruct(self):
        """Default migration deconstruct method"""
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
        """This migration does not change the state."""
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Create an AppConfigurationDefault instance with the provided data."""
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            full_key = '{}.{}'.format(app_label, self.key)
            default_config_model = from_state.apps.get_model('core', 'AppConfigurationDefault')
            config, _ = default_config_model.objects.get_or_create(key=full_key)
            if self.default_value is not None:
                config.default_value = self.default_value
            if self.choices is not None:
                config.choices = self.choices
            config.save()

    def describe(self):
        """Describe the migration."""
        return 'Creates or updates the default configuration value for an application.'
