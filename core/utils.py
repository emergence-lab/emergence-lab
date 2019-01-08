# -*- coding: utf-8 -*-
from datetimewidget.widgets import (
    DateWidget as _DateWidget,
    DateTimeWidget as _DateTimeWidget
)
from django import forms
from django_filters import LookupChoiceFilter


class DateWidget(_DateWidget):
    """Shim for DateWidget to fix signature for `render` method"""

    def render(self, name, value, renderer=None, attrs=None):
        return super().render(name, value, attrs)


class DateTimeWidget(_DateTimeWidget):
    """Shim for DateTimeWidget to fix signature for `render` method"""

    def render(self, name, value, renderer=None, attrs=None):
        return super().render(name, value, attrs)


DATE_LOOKUP_CHOICES = [
    ('exact', 'Equals'),
    ('lt', 'Less than'),
    ('lte', 'Less than/equal'),
    ('gt', 'Greater than'),
    ('gte', 'Greater than/equal')
]


class EnhancedDateFilter(LookupChoiceFilter):
    field_class = forms.DateField
