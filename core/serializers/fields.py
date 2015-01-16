# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType

from polymorphic.polymorphic_model import PolymorphicModel
from rest_framework import serializers


class PolymorphicDataField(serializers.Field):
    """
    Field representing the polymorphic data from a child class. Moves through
    the entire inheritance chain to the root class that inherits from
    PolymorphicModel and puts the data in a flat representation.
    """
    def __init__(self, *args, **kwargs):
        kwargs['source'] = '*'
        super(PolymorphicDataField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        model_class = ContentType.objects.get_for_id(obj.polymorphic_ctype_id).model_class()

        if model_class.__base__ is PolymorphicModel:
            return OrderedDict()

        polymorphic_fields = []

        while model_class.__base__ is not PolymorphicModel:
            parent_field = '{}_ptr'.format(
                model_class.__base__.__name__.lower())
            local_fields = model_class._meta.local_fields

            polymorphic_fields.extend(field.name
                                      for field in local_fields
                                      if field.name != parent_field)
            model_class = model_class.__base__

        return OrderedDict({field: getattr(obj, field)
                            for field in polymorphic_fields})


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
