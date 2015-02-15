# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.test import TestCase

from model_mommy import mommy
from rest_framework.serializers import ValidationError
from rest_framework.renderers import JSONRenderer

from core.models import Process, Sample, Substrate
from .models import ChildProcess, ParentProcess
from core.serializers import ProcessSerializer, SampleSerializer


class TestProcessSerializer(TestCase):

    def test_polymorphic_field_mapping(self):
        """
        Test that the polymorphic-specific properties are set correctly.
        * polymorphic_base_model should be equal to the model from Meta.model
        * polymorphic_derived_models should be a list of the models that are in
          the inheritance tree of the base model
        * polymorphic_class_mapping should map the class name to the model
          itself and a list of fields specific to that model.
        """
        serializer = ProcessSerializer()
        serializer._build_polymorphic_field_mapping()
        class_mapping = serializer.polymorphic_class_mapping
        self.assertEqual(serializer.Meta.model,
                         serializer.polymorphic_base_model)
        for subclass, field in [[ChildProcess, 'child_field'],
                                [ParentProcess, 'parent_field']]:
            self.assertIn(subclass, serializer.polymorphic_derived_models)
            self.assertIn(subclass.__name__, class_mapping)
            self.assertEqual(class_mapping[subclass.__name__].model, subclass)
            fields = [f.name for f in class_mapping[subclass.__name__].fields]
            self.assertEqual(fields, [field])

    def test_to_representation_base(self):
        """
        Test to_representation for the base Process class that the data is
        correct and it has all of the data.
        """
        process = mommy.make(Process)
        serializer = ProcessSerializer()
        representation = serializer.to_representation(process)
        self.assertEqual(process.uuid_full.hex, representation.get('uuid_full'))
        self.assertIsNotNone(representation.get('comment'))

    def test_to_representation_polymorphic_single(self):
        """
        Test to_representation for a derived process that defines an additional
        field. The representation should have all of the base fields in addition
        to the derived field.
        """
        process = mommy.make(ParentProcess)
        serializer = ProcessSerializer()
        representation = serializer.to_representation(process)
        self.assertEqual(process.uuid_full.hex, representation.get('uuid_full'))
        self.assertIsNotNone(representation.get('comment'))
        self.assertIsNotNone(representation.get('parent_field'))

    def test_to_representation_polymorphic_double(self):
        """
        Test to_representation for a derivation chain where each process defines
        their own fields. The representation should have all of the base fields
        as well as all of the polymorphic fields up the chain.
        """
        process = mommy.make(ChildProcess)
        serializer = ProcessSerializer()
        representation = serializer.to_representation(process)
        self.assertEqual(process.uuid_full.hex, representation.get('uuid_full'))
        self.assertIsNotNone(representation.get('comment'))
        self.assertIsNotNone(representation.get('parent_field'))
        self.assertIsNotNone(representation.get('child_field'))

    def test_to_internal_value_valid(self):
        """
        Test that passing the name of a derived class properly returns the
        class instance.
        """
        serializer = ProcessSerializer()
        model_class = serializer.to_internal_value('ChildProcess')
        self.assertEqual(model_class, ChildProcess)

    def test_to_internal_value_invalid(self):
        """
        Test that passing the name of a non-existant or non-derived class
        properly raises an exception.
        """
        serializer = ProcessSerializer()
        with self.assertRaises(ValidationError):
            serializer.to_internal_value('NonExistantClass')

    def test_create_base(self):
        """
        Test that the base instance of the class can be created.
        """
        serializer = ProcessSerializer()
        data = {
            'polymorphic_type': 'Process',
            'comment': 'Test comment',
        }
        process = serializer.create(data)
        self.assertIsNotNone(process)
        self.assertEqual(process.__class__, Process)
        self.assertEqual(process.comment, data['comment'])
        self.assertIsNotNone(process.uuid)

    def test_create_single(self):
        """
        Test that a singly derived instance of the class can be created.
        """
        serializer = ProcessSerializer()
        data = {
            'polymorphic_type': 'ParentProcess',
            'comment': 'Test comment',
            'parent_field': 111,
        }
        process = serializer.create(data)
        self.assertIsNotNone(process)
        self.assertEqual(process.__class__, ParentProcess)
        self.assertEqual(process.comment, data['comment'])
        self.assertEqual(process.parent_field, data['parent_field'])
        self.assertIsNotNone(process.uuid)

    def test_create_double(self):
        """
        Test that a doubly derived instance of the class can be created.
        """
        serializer = ProcessSerializer()
        data = {
            'polymorphic_type': 'ChildProcess',
            'comment': 'Test comment',
            'parent_field': 111,
            'child_field': 222,
        }
        process = serializer.create(data)
        self.assertIsNotNone(process)
        self.assertEqual(process.__class__, ChildProcess)
        self.assertEqual(process.comment, data['comment'])
        self.assertEqual(process.parent_field, data['parent_field'])
        self.assertEqual(process.child_field, data['child_field'])
        self.assertIsNotNone(process.uuid)


class TestSampleSerializer(TestCase):

    def test_serialization_sample(self):
        """
        Test serialization of only the sample fields.
        """
        sample = Sample.objects.create(substrate=mommy.make(Substrate),
                                       comment='comment')
        serializer = SampleSerializer(sample)
        self.assertEqual(serializer.data.get('uuid'), sample.uuid)
        self.assertEqual(serializer.data.get('comment'), sample.comment)

    def test_serialization_substrate(self):
        """
        Test serialization of the embedded substrate fields.
        """
        substrate = mommy.make(Substrate)
        sample = Sample.objects.create(substrate=substrate)
        serializer = SampleSerializer(sample)
        serialized_substrate = serializer.data.get('substrate')
        self.assertIsNotNone(serialized_substrate)
        self.assertEqual(serialized_substrate.get('serial'), substrate.serial)
