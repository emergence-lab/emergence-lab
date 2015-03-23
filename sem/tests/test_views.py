# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from model_mommy import mommy

from sem.models import SEMScan


class TestSEMScanCRUD(TestCase):

    def setUp(self):
        self.user_obj = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_create_sem(self):
        sem_obj = mommy.make(SEMScan,)
        sem_id = SEMScan.objects.all().first().id
        url = reverse('sem_detail', kwargs={'pk': sem_obj.id})
        match = resolve('/sem/{0}/'.format(sem_obj.id))
        response = self.client.get(url)
        self.assertEqual(match.url_name, 'sem_detail')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sem/sem_detail.html')

    def test_list_view(self):
        sem_obj_1 = mommy.make(SEMScan,)
        sem_obj_2 = mommy.make(SEMScan,)
        match = resolve('/sem/')
        url = reverse('sem_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sem/sem_list.html')
        self.assertEqual(len(response.context['object_list']),
                         len(SEMScan.objects.all()))
        self.assertEqual(match.url_name, 'sem_list')
