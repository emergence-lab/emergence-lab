# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import six


@python_2_unicode_compatible
class AppConfigurationDefault(models.Model):

    """Freeform application configuration key-value pairs.

    Applications can publish configuration keys via PublishAppConfiguration
    and they can be accessed anywhere
    """

    key = models.CharField(max_length=200, blank=False)
    default_value = models.CharField(max_length=200, blank=True)
    choices = ArrayField(models.CharField(max_length=200, blank=True), default=list)

    def __str__(self):
        return '{}: {} {}'.format(self.key, self.default_value, self.choices)


def get_configuration_default(key):
    """Return the default value for the provided configuration key.

    :param key: The key to lookup - must be formatted as 'appname.keyname'.
    :returns: The default value for the specified key. If no default was
              provided then returns an empty string.
    :raises TypeError: If the key is not a string type
    :raises ValueError: If the key is an empty string
    :raises ValueError: If the key is not properly formatted
    """
    if not isinstance(key, six.string_types):
        raise TypeError('key must be a string')
    if not key:
        raise ValueError('key must not be an empty string')
    if '.' not in key:
        raise ValueError('key must be formatted as appname.keyname')

    config = AppConfigurationDefault.objects.get(key=key)
    return config.default_value


def get_configuration_choices(key):
    """Return a list of possible values for the provided configuration key.

    :param key: The key to lookup - must be formatted as 'appname.keyname'.
    :returns: The possible choices for values for the specified key. If no
              choices were provided then returns an empty list.
    :raises TypeError: If the key is not a string type
    :raises ValueError: If the key is an empty string
    :raises ValueError: If the key is not properly formatted
    """
    if not isinstance(key, six.string_types):
        raise TypeError('key must be a string')
    if not key:
        raise ValueError('key must not be an empty string')
    if '.' not in key:
        raise ValueError('key must be formatted as appname.keyname')

    config = AppConfigurationDefault.objects.get(key=key)
    return config.choices


def list_configuration_keys(app_name=None):
    """Return a list of defined configuration keys.

    :param app_name: Optional. Limits returned keys to only those defined by the
                     specified application. Set to None by default.
    :returns: The list of defined configuration keys. If app_name is specified
              then only returns configuration keys defined by that application.
    :raises TypeError: If the application name is defined and not a string type
    :raises ValueError: If the application name is an empty string
    """
    if app_name is not None:
        if not isinstance(app_name, six.string_types):
            raise TypeError('app_name must be a string')
        if not app_name:
            raise ValueError('app_name must not be an empty string')

        return list(AppConfigurationDefault.objects.filter(key__startswith=app_name + '.')
                                                   .values_list('key', flat=True))
    return list(AppConfigurationDefault.objects.all().values_list('key', flat=True))


@python_2_unicode_compatible
class InstanceConfiguration(models.Model):

    """Per-instance configuration via key-value pairs.

    Provides a minimal dict-like interface. Will return default values
    (if defined) and the value was not overridden on this instance.
    """

    configuration = JSONField(default=dict)

    def __str__(self):
        return str(self.configuration)

    def __contains__(self, key):
        """Return if the key is a defined configuration key.

        :param key: The key to lookup - should be formatted as 'appname.keyname'.
        :returns: True if the key is defined, else False.
        """
        return key in self.configuration or key in list_configuration_keys()

    def __getitem__(self, key):
        """Return the value for the specified configuration key.

        Returns the per-instance value if defined, otherwise returns the default.

        :param key: The key to lookup - should be formatted as 'appname.keyname'.
        :returns: The value (or default value) for the configuration key
        :raises KeyError: If the configuration key is not defined.
        """
        if key in self.configuration:
            return self.configuration[key]
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
        self.configuration[key] = value
        self.save()
