# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test import TestCase

from model_mommy import mommy

from core.tests.helpers import test_resolution_template
from core.models import Process, Sample, Substrate
from afm.models import AFMFile, AFMScan


class TestAFMCRUD(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_afm_list_resolution_template(self):
        test_resolution_template(self,
            '/afm/',
            'afm_list',
            'afm/afm_list.html',
            200)

    def test_afm_list_content(self):
        afm = mommy.make(AFMScan)
        url = reverse('afm_list')
        response = self.client.get(url)
        self.assertContains(response, afm.uuid)

    def test_afm_detail_resolution_template(self):
        afm = mommy.make(AFMScan)
        test_resolution_template(self,
            '/afm/{}/'.format(afm.uuid),
            'afm_detail',
            'afm/afm_detail.html',
            200)

    def test_afm_detail_content(self):
        afm = mommy.make(AFMScan)
        url = reverse('afm_detail', args=(afm.uuid,))
        response = self.client.get(url)
        self.assertContains(response, afm.uuid)

    def test_afm_create_resolution_template(self):
        test_resolution_template(self,
            '/afm/create/',
            'afm_create',
            'afm/afm_create.html',
            200)

    def test_afm_update_resolution_template(self):
        afm = mommy.make(AFMScan)
        test_resolution_template(self,
            '/afm/{}/update/'.format(afm.uuid),
            'afm_update',
            'afm/afm_update.html',
            200)

    def test_afm_create_valid_data(self):
        url = reverse('afm_create')
        data = {'comment': 'testing'}
        response = self.client.post(url, data)
        afm = AFMScan.objects.last()
        self.assertEqual(afm.comment, data['comment'])
        detail_url = reverse('afm_detail', args=(afm.uuid,))
        self.assertRedirects(response, detail_url)

    def test_afm_update_valid_data(self):
        afm = mommy.make(AFMScan)
        url = reverse('afm_update', args=(afm.uuid,))
        data = {'comment': 'testing'}
        response = self.client.post(url, data)
        afm = AFMScan.objects.get(id=afm.id)
        self.assertEqual(afm.comment, data['comment'])
        detail_url = reverse('afm_detail', args=(afm.uuid,))
        self.assertRedirects(response, detail_url)
