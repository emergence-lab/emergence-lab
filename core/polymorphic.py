# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import namedtuple


PolymorphicClassInfo = namedtuple('PolymorphicClassInfo', [
    'model',
    'fields',
])


def get_subclasses(cls):
    """
    Recursively creates a list of all subclasses of the provided class.
    """
    return cls.__subclasses__() + [sub
                                   for direct in cls.__subclasses__()
                                   for sub in get_subclasses(direct)]


def get_polymorphic_field_mapping(cls):
    """
    Creates several helper attributes on the serializer and builds a
    mapping of subclasses to the fields included on each.
    """
    return {
        subclass.__name__: PolymorphicClassInfo(
            model=subclass,
            fields=[field for field in subclass._meta.local_fields
                    if field.serialize and not field.rel])
        for subclass in get_subclasses(cls)
    }
