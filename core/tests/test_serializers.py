# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import unittest

from model_mommy import mommy

from core.models import Process
from .models import ChildProcess, ParentProcess
from core.serializers import ProcessSerializer


class TestProcessSerializer(unittest.TestCase):

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
