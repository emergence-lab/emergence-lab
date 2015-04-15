# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from model_mommy import mommy

from hall.models import Hall


class TestSEMScanCRUD(TestCase):

    def setUp(self):
        self.user_obj = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_create_hall(self):
        hall_obj = mommy.make(Hall,)
        hall_id = Hall.objects.all().first().id
        url = reverse('hall_detail', kwargs={'pk': hall_obj.id})
        match = resolve('/hall/{0}/'.format(hall_obj.id))
        response = self.client.get(url)
        self.assertEqual(match.url_name, 'hall_detail')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hall/hall_detail.html')

    def test_list_view(self):
        hall_obj_1 = mommy.make(Hall,)
        hall_obj_2 = mommy.make(Hall,)
        match = resolve('/hall/')
        url = reverse('hall_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hall/hall_list.html')
        self.assertEqual(len(response.context['object_list']),
                         len(Hall.objects.all()))
        self.assertEqual(match.url_name, 'hall_list')
