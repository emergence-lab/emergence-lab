# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers


class PolymorphicTypeField(serializers.Field):
    """
    Field representing the name of the polymorphic class. Used to help identify
    what data should be availiable in the PolymorphicDataField representation.
    """

    def __init__(self, *args, **kwargs):
        kwargs['source'] = 'polymorphic_ctype'
        super(PolymorphicTypeField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        return obj.model_class().__name__
