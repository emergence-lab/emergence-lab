# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from polymorphic.polymorphic_model import PolymorphicModel
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_field_kwargs


class PolymorphicModelSerializer(serializers.ModelSerializer):
    """
    Serializer to display data up the entire inheritance chain in a flat
    representation. Currently does not support relational fields.
    """

    def to_representation(self, obj):
        ret = super(PolymorphicModelSerializer, self).to_representation(obj)

        model_class = ContentType.objects.get_for_id(obj.polymorphic_ctype_id).model_class()
        if model_class is not PolymorphicModel:
            while model_class.__base__ is not PolymorphicModel:
                local_fields = model_class._meta.local_fields

                polymorphic_fields = {field.name: field
                                      for field in local_fields
                                      if field.serialize and not field.rel}

                for field_name, model_field in polymorphic_fields.items():
                    rest_field = self._field_mapping[model_field]
                    kwargs = get_field_kwargs(field_name, model_field)
                    if 'choices' in kwargs:
                        rest_field = serializers.ChoiceField
                    if not issubclass(rest_field, serializers.ModelField):
                        kwargs.pop('model_field', None)
                    if (not issubclass(rest_field, serializers.CharField) and
                            not issubclass(rest_field, serializers.ChoiceField)):
                        kwargs.pop('allow_blank', None)
                    field = rest_field(**kwargs)
                    attribute = getattr(obj, field_name)
                    if attribute is None:
                        ret[field_name] = None
                    else:
                        ret[field_name] = field.to_representation(attribute)

                model_class = model_class.__base__

        return ret
