# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.db import router
from django.db.migrations.operations.base import Operation


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
        :raises ValueError: If the key is an empty string or contains a '.'
        :raises TypeError: If choices is not a list, tuple, or None
        :raises TypeError: If the items in choices are not strings
        :raises ValueError: If default_value is not a valid choice
        """
        if re.match(r'^((?![\.\\])[\w\d\-])+$', key) is None:
            raise ValueError('invalid key "{}"'.format(key))

        if choices is not None:
            if not isinstance(choices, (list, tuple)):
                raise TypeError('choices must be a list or tuple')

        if choices is not None and default_value is not None:
            if default_value not in choices:
                raise ValueError('default_value must be a valid choice')

        self.key = key
        self.default_value = default_value
        self.choices = choices

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
