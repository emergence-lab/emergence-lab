# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from copy import copy

from django.contrib.contenttypes.models import ContentType

from polymorphic.polymorphic_model import PolymorphicModel
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_field_kwargs
import six

from .fields import PolymorphicTypeField
from core.polymorphic import get_subclasses, get_polymorphic_field_mapping


class PolymorphicModelSerializer(serializers.ModelSerializer):
    """
    Serializer to display data up the entire inheritance chain in a flat
    representation. Currently does not support relational fields.

    Uses the field polymorphic_type to store the name of the class.
    """
    def __init__(self, *args, **kwargs):
        super(PolymorphicModelSerializer, self).__init__(*args, **kwargs)
        self._build_polymorphic_field_mapping()
        self.fields['polymorphic_type'] = PolymorphicTypeField()

    @property
    def polymorphic_fields(self):
        """
        A dictionary of {field_name: field_instance} for polymorphic fields.
        """
        if not hasattr(self, '_polymorphic_fields'):
            self._polymorphic_fields = {}
            for key, value in six.iteritems(self.get_polymorphic_fields()):
                self._polymorphic_fields[key] = value
        return self._polymorphic_fields

    def get_polymorphic_fields(self):
        """
        returns a dictionary of {field_name: field_instance} for polymorphic
        fields.
        """
        if not self.polymorphic_class_mapping:
            self._build_polymorphic_field_mapping()

        polymorphic_fields = OrderedDict()

        for name, subclass in six.iteritems(self.polymorphic_class_mapping):
            for field in subclass.fields:
                rest_field = self._field_mapping[field]
                kwargs = get_field_kwargs(field.name, field)
                if 'choices' in kwargs:
                    rest_field = serializers.ChoiceField
                if not issubclass(rest_field, serializers.ModelField):
                    kwargs.pop('model_field', None)
                if (not issubclass(rest_field, serializers.CharField) and
                        not issubclass(rest_field, serializers.ChoiceField)):
                    kwargs.pop('allow_blank', None)

                polymorphic_fields[field.name] = rest_field(**kwargs)

        return polymorphic_fields

    def to_representation(self, obj):
        if not self.polymorphic_class_mapping:
            self._build_polymorphic_field_mapping()

        model_class = ContentType.objects.get_for_id(obj.polymorphic_ctype_id).model_class()
        if model_class is not PolymorphicModel:

            while model_class.__base__ is not PolymorphicModel:

                for field in self.polymorphic_class_mapping[model_class.__name__].fields:
                    self.fields[field.name] = copy(self.polymorphic_fields[field.name])

                model_class = model_class.__base__

        return super(PolymorphicModelSerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        if not self.polymorphic_class_mapping:
            self._build_polymorphic_field_mapping()

        model_name = validated_data.pop('polymorphic_type')
        model_class = self.polymorphic_class_mapping[model_name].model
        instance = model_class.objects.create(**validated_data)
        return instance

    def _build_polymorphic_field_mapping(self):
        model = self.Meta.model
        self.polymorphic_base_model = model
        self.polymorphic_derived_models = get_subclasses(model)
        self.polymorphic_class_mapping = get_polymorphic_field_mapping(model)
