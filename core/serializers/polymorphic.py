# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import namedtuple, OrderedDict
from copy import copy

from django.contrib.contenttypes.models import ContentType

from polymorphic.polymorphic_model import PolymorphicModel
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_field_kwargs
import six

from .fields import PolymorphicTypeField


PolymorphicClassInfo = namedtuple('PolymorphicClassInfo', [
    'model',
    'fields',
])


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
        pass

    def _build_polymorphic_field_mapping(self):
        """
        Creates several helper attributes on the serializer and builds a
        mapping of subclasses to the fields included on each.
        """
        model = self.Meta.model
        self.polymorphic_base_model = model
        self.polymorphic_derived_models = self._all_subclasses(model)

        self.polymorphic_class_mapping = {
            subclass.__name__: PolymorphicClassInfo(
                model=subclass,
                fields=[field for field in subclass._meta.local_fields
                        if field.serialize and not field.rel])
            for subclass in self.polymorphic_derived_models
        }

    def _all_subclasses(self, cls):
        """
        Recursively creates a list of all subclasses of the provided class.
        """
        return cls.__subclasses__() + [sub
                                       for direct in cls.__subclasses__()
                                       for sub in self._all_subclasses(direct)]
