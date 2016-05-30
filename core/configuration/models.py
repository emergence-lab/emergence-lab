# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


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


@python_2_unicode_compatible
class AppConfigurationSubscription(models.Model):

    model = models.ForeignKey(ContentType)

    def __str__(self):
        return str(self.model)


def get_configuration_default(key):
    """Return the default value for the provided configuration key.

    :param key: The key to lookup - must be formatted as 'appname_keyname'.
    :returns: The default value for the specified key. If no default was
              provided then returns an empty string.
    """
    config = AppConfigurationDefault.objects.get(key=key)
    return config.default_value


def get_configuration_choices(key):
    """Return a list of possible values for the provided configuration key.

    :param key: The key to lookup - must be formatted as 'appname_keyname'.
    :returns: The possible choices for values for the specified key. If no
              choices were provided then returns an empty list.
    """
    config = AppConfigurationDefault.objects.get(key=key)
    return config.choices


def list_configuration_keys(app_name=None):
    """Return a list of defined configuration keys.

    :param app_name: Optional. Limits returned keys to only those defined by the
                     specified application. Set to None by default.
    :returns: The list of defined configuration keys. If app_name is specified
              then only returns configuration keys defined by that application.
    """
    if app_name is not None:
        return list(AppConfigurationDefault.objects.filter(key__startswith=app_name + '_')
                                                   .values_list('key', flat=True))
    return list(AppConfigurationDefault.objects.all().values_list('key', flat=True))
