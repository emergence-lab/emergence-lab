from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_not_zero(value):
    if value <= 0:
        raise ValidationError(_('This value cannot be less than 1'))
