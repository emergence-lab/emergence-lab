# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools

from django import forms

from .models import get_configuration_choices


def _get_configuration_choices_form(key):
    """Build list of tuples of configuration keys for use in ChoiceField."""
    choices = get_configuration_choices(key)
    if not choices:
        raise ValueError('key "{}" does not limit values to any choices'.format(key))
    return [(c, c.title()) for c in choices]


def build_configuration_choices(key):
    return functools.partial(_get_configuration_choices_form, key)


class ConfigurationChoiceField(forms.ChoiceField):

    """ChoiceField that build choices based on those for a configuration key."""

    def __init__(self, key, *args, **kwargs):
        self.key = key
        kwargs['choices'] = functools.partial(_get_configuration_choices_form, key)
        super(ConfigurationChoiceField, self).__init__(*args, **kwargs)
