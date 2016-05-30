# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import JSONField


class ConfigurationField(JSONField):

    """Wrapper field for JSONField that uses ConfigurationDict in python."""

    def __init__(self, *args, **kwargs):
        """Set default to ConfigurationDict."""
        if 'default' not in kwargs:
            kwargs['default'] = dict
        super(ConfigurationField, self).__init__(*args, **kwargs)
