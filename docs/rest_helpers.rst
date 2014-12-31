=============================
Django REST Framework Helpers
=============================

The core models use more advanced Django model concepts such as polymorphic and tree-based models. These concepts are not supported by Django REST Framework by default or by any third party module that was able to be located. In lieu of an official or semi-official solution, we have developed an in-house solution for both model types. The goals of both are to support easy and intutitive configuration for (de)serialization and complex configurations.

Polymorphic Models
==================

Serialization or de-serialization of polymorphic models is a critical feature for the REST API. The default behavior for django-polymorphicis to create a heterogeneous queryset where each item is the final derived type rather than the base type. This is one of the major features of the module over regular Django model inheritance. Recreating this behavior in Django REST Framework is the goal. A list API endpoint should be able to display the relevant information in a heterogeneous manner if desired.

------------------------------
``PolymorphicModelSerializer``
------------------------------

Django REST Framework provides a convenient helper base class ``ModelSerializer`` to inspect the model class to find out the model fields and intelligently guess the corresponding REST field to use in the serializer. This automatic behavior fails for polymorphic models as it can only look into the base class that the serializer is created for. The ``PolymorphicModelSerializer`` allows inspection of the entire inheritance chain and populates the fields accordingly as needed.

The default behavior of ``ModelSerializer`` may be customized in three ways, which can all be mixed and matched.

1. Explicitly declaring fields in the serializer class and tying them to specific model fields.
2. Specifying which fields should be included using the ``Meta.fields`` attribute, where any field unmentioned will not be serialized.
3. Specifying which fields should be excluded using the ``Meta.exclude`` attribute, where any fields unmentioned will be included for serialization.

This behavior is supported by the ``PolymorphicModelSerializer`` in all of the three above ways. Two new options are included in the ``Meta`` subclass of the serializer: ``polymorphic_fields`` and ``polymorphic_exclude``, which correspond directly in behavior to the ``fields`` and ``exclude`` attributes from the regular ``ModelSerializer``, but for fields from the derived polymorphic classes. The usage of all of these ``Meta`` options in the ``PolymorphicModelSerializer`` is as follows:

* ``Meta.fields``: Used to include fields from the base model (specified in ``Meta.model``). List or tuple of strings corresponding to the field names.
* ``Meta.exclude``: Used to exclude fields from the base model. List or tuple of strings correspondin to the field names.
* ``Meta.polymorphic_fields``: Used to include fields from the derived models. Dictionary where the keys are the names of the derived classes (via ``__name__``) and the values are a list or tuple of strings corresponding to the field names.
* ``Meta.polymorphic_exclude``: Used to exclude fields from the derived models. Dictionary where the keys are the names of the derived classes (via ``__name__``) and the values are a list or tuple of strings corresponding to the field names.

In order to assist in deserialization, ``PolymorphicModelSerializer`` includes an additional field ``polymorphic_type`` which corresponds to the name of the class that the data represents.
