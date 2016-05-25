# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import JSONField

from configuration.models import (
    get_configuration_default,
    get_configuration_choices,
    list_configuration_keys,
)

import six


class ConfigurationDict(dict):

    def __contains__(self, key):
        """Return if the key is a defined configuration key.

        :param key: The key to lookup - should be formatted as 'appname.keyname'.
        :returns: True if the key is defined, else False.
        """
        return key in self._dict or key in list_configuration_keys()


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

        if key in self._dict:
            return self._dict[key]
        elif key in list_configuration_keys():
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

        self._dict[key] = value

    def __delitem__(self, key):
        """Reset the instance value to default for the specified configuration key.

        :param key: The key to reset the value for - should be formatted as 'appname.keyname'.
        :raises TypeError: If the configuration key is not a string.
        :raises KeyError: If the configuration key is not defined.
        """
        if not isinstance(key, six.string_types):
            raise TypeError('Keys must be strings')

        if key not in list_configuration_keys():
            raise KeyError('Configuration key "{}" is not defined'.format(key))

        del self._dict[key]


class ConfigurationField(JSONField):

    def from_db_value(self, value, expression, connection, context):
        return ConfigurationDict(value)

    def get_prep_value(self, value):
        return super(ConfigurationField, self).get_prep_value(value._dict)
