# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy

from core.forms import SampleSelectOrCreateForm, TrackProjectForm
from core.models import Project, Sample, Substrate


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


class TestTrackProjectForm(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        cls.user = User.objects.create_user('username', password='')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()

    def test_save(self):
        project = mommy.make(Project)
        form = TrackProjectForm(data={
            'project': project.id,
            'is_owner': True,
        })
        tracking = form.save(user=self.user)
        self.assertEqual(project.id, tracking.project_id)
        self.assertEqual(self.user.id, tracking.user_id)
        self.assertTrue(tracking.is_owner)
