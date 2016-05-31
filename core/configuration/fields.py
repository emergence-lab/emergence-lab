# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import JSONField

from .models import AppConfigurationDefault


def build_configuration_default():
    """Return dictionary with existing configuration keys and default values."""
    default = {}
    for config in AppConfigurationDefault.objects.all():
        default[config.key] = config.default_value
    return default


class ConfigurationField(JSONField):

    """Wrapper field for JSONField that uses ConfigurationDict in python."""

    def __init__(self, *args, **kwargs):
        """Set default to ConfigurationDict."""
        if 'default' not in kwargs:
            kwargs['default'] = build_configuration_default
        super(ConfigurationField, self).__init__(*args, **kwargs)
