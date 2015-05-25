# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.forms import ValidationError
from django.test import TestCase

from model_mommy import mommy

from core.models import Process, Sample, Substrate


class TestAFMUpload(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_autocreate_resolution_template(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = '/afm/autocreate/{}/'.format(sample.uuid)
        match = resolve(url)
        self.assertEqual(match.url_name, 'afm_autocreate')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/process_create.html')
        self.assertEqual(response.status_code, 200)

    def test_autocreate_valid_data(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('afm_autocreate', args=[sample.uuid])
        data = {
            'pieces': ['a'],
            'type': 'afm',
        }
        response = self.client.post(url, data)
        process = Process.objects.last()
        self.assertRedirects(response, reverse('afm_upload', args=[process.uuid]))

    def test_upload_resolution_template(self):
        process = mommy.make(Process, type_id='afm')
        url = '/afm/{}/upload/'.format(process.uuid)
        match = resolve(url)
        self.assertEqual(match.url_name, 'afm_upload')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/process_upload.html')
        self.assertEqual(response.status_code, 200)
