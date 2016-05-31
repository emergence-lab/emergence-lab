# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.db import router
from django.db.migrations.operations.base import Operation

import six


class PublishConfiguration(Operation):

    """Migration to publish configuration key for an application.

    Creates a AppConfigurationDefault object. Configuration keys once published
    can be accessed anywhere by 'appname_keyname' and can be overridden on a
    per-instance basis.
    """

    reversible = False
    reduces_to_sql = False
    atomic = False
    elidable = False

    def __init__(self, key, default_value=None, choices=None):
        """Create app configuration object.

        :param key: The name of the configuration key
        :param default_value: Optional. The default value for the key. Defaults
                              to empty string if parameter is None.
        :param choices: Optional. The possible valid choices for values. Defaults
                        to empty list if parameter is None, which means any value
                        is valid.
        :raises ValueError: If the key is an empty or invalid string
        :raises TypeError: If the default_value is not a string or None
        :raises TypeError: If choices is not a list, tuple, or None
        :raises TypeError: If the items in choices are not strings
        :raises ValueError: If default_value is not a valid choice
        """
        default_value = default_value or ''
        choices = choices or []

        if re.match(r'^[a-zA-Z0-9_]+$', key) is None:
            raise ValueError('invalid key "{}"'.format(key))

        if not isinstance(default_value, six.string_types):
            raise TypeError('default_value must be a string')

        if not isinstance(choices, (list, tuple)):
            raise TypeError('choices must be a list or tuple')
        if not all(isinstance(choice, six.string_types) for choice in choices):
            raise TypeError('choice options must be strings')

        if default_value and choices and default_value not in choices:
            raise ValueError('default_value must be a valid choice')

        self.key = key
        self.default_value = default_value
        self.choices = choices

    def deconstruct(self):
        """Default migration deconstruct method."""
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
        """Make no changes to the state."""
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Create an AppConfigurationDefault instance with the provided data."""
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            full_key = '{}_{}'.format(app_label, self.key)
            default_config_model = from_state.apps.get_model(
                'configuration', 'AppConfigurationDefault')
            config, _ = default_config_model.objects.get_or_create(key=full_key)
            config.default_value = self.default_value
            config.choices = self.choices
            config.save()

            # add this configuration key to all subscribers
            subscription = from_state.apps.get_model(
                'configuration', 'AppConfigurationSubscription')
            for obj in subscription.objects.all():
                subscriber_model = from_state.apps.get_model(obj.app_label, obj.model_name)
                for subscriber in subscriber_model.objects.all():
                    subscriber.configuration[full_key] = self.default_value
                    subscriber.save()

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        """Raise exception since migration cannot be reversed."""
        raise NotImplementedError('This migration cannot be reversed.')

    def describe(self):
        """Describe the migration."""
        return 'Creates or updates the default configuration value for an application.'


class ConfigurationSubscribe(Operation):

    """Operation to subscribe a model for to configuration."""

    reversible = True
    reduces_to_sql = False
    atomic = False
    elidable = False

    def __init__(self, model_name, field_name):
        """Create ConfigurationSubscribe object."""
        self.model_name = model_name
        self.field_name = field_name

    def deconstruct(self):
        """Default migration deconstruct method."""
        return (
            self.__class__.__name__,
            [],
            {
                'model_name': self.model_name,
                'field_name': self.field_name,
            }
        )

    def state_forwards(self, app_label, state):
        """Make no changes to the state."""
        pass

    def state_backwards(self, app_label, state):
        """Make no changes to the state."""
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Create subscription object and copy all existing configuration over."""
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            # create AppConfigurationSubscription object
            subscription = from_state.apps.get_model(
                'configuration', 'AppConfigurationSubscription')
            subscription.objects.create(app_label=app_label, model_name=self.model_name)

            # for each object of the subscriber model, add all existing configuration
            subscriber = from_state.apps.get_model(app_label, self.model_name)
            configuration = from_state.apps.get_model(
                'configuration', 'AppConfigurationDefault')
            self._add_existing_configuration(subscriber, configuration)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        """Remove model as a subscriber."""
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            subscription = from_state.apps.get_model(
                'configuration', 'AppConfigurationSubscription')
            subscriber = subscription.objects.get(app_label=app_label,
                                                  model_name=self.model_name)
            subscriber.delete()

    def _add_existing_configuration(self, subscriber, configuration):
        """Add all existing configuration to all instances of subscriber model."""
        for obj in subscriber.objects.all():
            for config in configuration.objects.all():
                getattr(obj, self.field_name)[config.key] = config.default_value
            obj.save()
