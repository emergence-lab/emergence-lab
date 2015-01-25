# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from model_mommy import mommy

from core.forms import SampleSelectOrCreateForm
from core.models import Sample, Substrate


class TestSampleSelectOrCreateForm(TestCase):

    def test_clean_specify_nonexistant_sample(self):
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': 's0001',
        })
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('__all__'))
        self.assertListEqual(errors.get('__all__'),
                             ['Sample s0001 not found'])

    def test_clean_specify_existing(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': sample.uuid,
        })
        errors = dict(form.errors)
        self.assertDictEqual(errors, {})

    def test_clean_specify_existing_and_new(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        form = SampleSelectOrCreateForm(data={
            'sample_uuid': sample.uuid,
            'sample_comment': 'sample comment',
            'substrate_comment': 'substrate comment',
            'substrate_serial': 'substrate serial',
            'substrate_source': 'substrate source',
        })
        errors = dict(form.errors)
        self.assertIsNotNone(errors.get('__all__'))
        self.assertListEqual(errors.get('__all__'),
                             ['Existing sample cannot be specified in '
                              'addition to creating a new sample'])

    def test_clean_new_sample(self):
        form = SampleSelectOrCreateForm(data={
            'sample_comment': 'sample comment',
            'substrate_comment': 'substrate comment',
            'substrate_serial': 'substrate serial',
            'substrate_source': 'substrate source',
        })
        errors = dict(form.errors)
        self.assertDictEqual(errors, {})
