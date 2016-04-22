# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from core.tests.helpers import test_resolution_template
from core.models import Process, Sample, Substrate


class TestAFMUpload(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_autocreate_resolution_template(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        test_resolution_template(self,
            url='/afm/autocreate/{}/'.format(sample.uuid),
            url_name='afm_autocreate',
            template_file='core/process_create.html',
            response_code=200)

    def test_autocreate_valid_data(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        url = reverse('afm_autocreate', args=[sample.uuid])
        data = {
            'title': 'process title',
            'pieces': ['a'],
            'type': 'afm',
        }
        response = self.client.post(url, data)
        process = Process.objects.last()
        self.assertRedirects(response, reverse('afm_upload', args=[process.uuid]))

    def test_upload_resolution_template(self):
        process = mommy.make(Process, type_id='afm')
        test_resolution_template(self,
            url='/afm/{}/upload/'.format(process.uuid),
            url_name='afm_upload',
            template_file='core/process_upload.html',
            response_code=200)
