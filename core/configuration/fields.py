# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import JSONField

from .models import (
    get_configuration_default,
    get_configuration_choices,
    list_configuration_keys,
)

import six


class ConfigurationDict(dict):

    """Dictionary wrapper object for defined configuration keys.

    Limits keys to defined configuration keys. Pulls values from instance with
    fallback to default (if defined) values.
    """

    def __contains__(self, key):
        """Return if the key is a defined configuration key.

        :param key: The key to lookup - should be formatted as 'appname.keyname'.
        :returns: True if the key is defined, else False.
        """
        return key in list_configuration_keys()

    def __getitem__(self, key):
        """Return the value for the specified configuration key.

        Returns the per-instance value if defined, otherwise returns the default.

        :param key: The key to lookup - should be formatted as 'appname.keyname'.
        :returns: The value (or default value) for the configuration key
        :raises TypeError: If the configuration key is not a string.
        :raises KeyError: If the configuration key is not defined.
        """
        if not isinstance(key, six.string_types):
            raise TypeError('Keys must be strings')

        if dict.__contains__(self, key):  # get overridden value
            return dict.__getitem__(self, key)
        elif key in list_configuration_keys():  # get default value
            return get_configuration_default(key)
        else:
            raise KeyError('Configuration key "{}" is not defined'.format(key))

    def __setitem__(self, key, value):
        """Set the instance value for the specified configuration key.

        If choices were specified, then value should be a valid choice.

        :param key: The key to set the value for - should be formatted as 'appname.keyname'.
        :param value: The value to set for the configuration key
        :raises KeyError: If the configuration key is not defined.
        :raises ValueError: If the configuration key is not a valid choice.
        """
        if key not in list_configuration_keys():
            raise KeyError('Configuration key "{}" is not defined'.format(key))

        choices = get_configuration_choices(key)
        if choices and value not in choices:
            raise ValueError(
                'Configuration value "{}" for key "{}" is not a valid choice. '
                'Valid options include {}.'.format(value, key, choices))

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        """Reset the instance value to default for the pecified configuration key.

        :param key: The key to reset the value for - should be formatted as 'appname.keyname'.
        :raises TypeError: If the configuration key is not a string.
        :raises KeyError: If the configuration key is not defined.
        """
        if not isinstance(key, six.string_types):
            raise TypeError('Keys must be strings')

        if key not in list_configuration_keys():
            raise KeyError('Configuration key "{}" is not defined'.format(key))

        dict.__delitem__(self, key)


class ConfigurationField(JSONField):

    """Wrapper field for JSONField that uses ConfigurationDict in python."""

    def __init__(self, *args, **kwargs):
        """Set default to ConfigurationDict."""
        if 'default' not in kwargs:
            kwargs['default'] = ConfigurationDict
        super(ConfigurationField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        """Convert value to ConfigurationDict."""
        try:
            value = ConfigurationDict(value)
        except TypeError:
            value = ConfigurationDict()
        return value

    def get_prep_value(self, value):
        """Defer to JSONField implementation."""
        return super(ConfigurationField, self).get_prep_value(value)
