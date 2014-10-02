# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from model_mommy import mommy

from core.models import project, investigation
from growths.models import growth, sample


class TestGrowthView(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        user = User.objects.create_user('default', password='')
        mommy.make('core.operator', user=user)

        proj = mommy.make(project, name='project 1', slug='project-1')
        invest = mommy.make(investigation, name='invest 1',
                            slug='invest-1', project=proj)
        cls.g1000 = mommy.make(growth, growth_number='g1000', project=proj,
                               investigation=invest)
        cls.g1001 = mommy.make(growth, growth_number='g1001', project=proj,
                               investigation=invest)
        for pocket in range(1, 7):
            smpl = mommy.make(sample, growth=cls.g1000,
                              pocket=pocket, piece='')
            smpl.parent = smpl
            smpl.save()
        smpl = mommy.make(sample, growth=cls.g1001, parent=smpl,
                          pocket=1, piece='')
        smpl.split(3)

    @classmethod
    def tearDownClass(cls):
        sample.objects.all().delete()
        growth.objects.all().delete()
        investigation.objects.all().delete()
        project.objects.all().delete()
        get_user_model().objects.all().delete()

    def setUp(self):
        self.client.login(username='default', password='')

    def test_growth_detail_resolution_template(self):
        url = '/{0}/'.format(self.g1000.growth_number)
        match = resolve(url)
        self.assertEqual(match.url_name, 'growth_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/growth_detail.html')

    def test_growth_detail_content(self):
        url = reverse('growth_detail', args=(self.g1000.growth_number,))
        response = self.client.get(url)
        self.assertContains(response, self.g1000.growth_number)

    def test_sample_detail_resolution_template(self):
        obj = sample.objects.filter(growth__growth_number='g1001').first()
        url = '/sample/{0}/'.format(obj.id)
        match = resolve(url)
        self.assertEqual(match.url_name, 'sample_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/sample_detail.html')

    def test_sample_detail_content(self):
        obj = sample.objects.filter(growth__growth_number='g1001').first()
        url = reverse('sample_detail', args=(obj.id,))
        response = self.client.get(url)
        self.assertContains(response, obj.__str__())

    def test_sample_family_detail_resolution_template(self):
        obj = sample.objects.filter(growth__growth_number='g1001').first()
        url = '/{0}/{1}/'.format(self.g1001.growth_number, obj.pocket)
        match = resolve(url)
        self.assertEqual(match.url_name, 'sample_family_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/sample_family_detail.html')

    def test_sample_family_detail_content(self):
        obj = sample.objects.filter(growth__growth_number='g1001').first()
        url = reverse('sample_family_detail', args=(self.g1001.growth_number,
                                                    obj.pocket))
        response = self.client.get(url)
        for obj in sample.objects.filter(growth__growth_number='g1001'):
            self.assertContains(response, obj.__str__())

    def test_growth_update_resolution_template(self):
        obj = mommy.make(growth, growth_number='g1002',
                         project=self.g1000.project,
                         investigation=self.g1000.investigation)
        url = '/{0}/update/'.format(obj.growth_number)
        match = resolve(url)
        self.assertEqual(match.url_name, 'growth_update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/growth_update.html')

    def test_growth_update_valid_data(self):
        obj = mommy.make(growth, growth_number='g1002',
                         project=self.g1000.project,
                         investigation=self.g1000.investigation)
        url = reverse('growth_update', args=(obj.growth_number,))
        data = {'run_comments': 'test comment'}
        response = self.client.post(url, data)
        obj = growth.objects.get(id=obj.id)
        self.assertEqual(obj.run_comments, data['run_comments'])
        detail_url = reverse('growth_detail', args=(obj.growth_number,))
        self.assertRedirects(response, detail_url)

    def test_sample_update_resolution_template(self):
        obj = mommy.make(sample, growth=self.g1001, pocket=2)
        obj.parent = obj
        obj.save()
        url = '/sample/{0}/update/'.format(obj.id)
        match = resolve(url)
        self.assertEqual(match.url_name, 'sample_update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/sample_update.html')

    def test_sample_update_valid_data(self):
        obj = mommy.make(sample, growth=self.g1001, pocket=2)
        obj.parent = obj
        obj.save()
        url = reverse('sample_update', args=(obj.id,))
        data = {'comment': 'test comment'}
        response = self.client.post(url, data)
        obj = sample.objects.get(id=obj.id)
        self.assertEqual(obj.comment, data['comment'])
        detail_url = reverse('sample_detail', args=(obj.id,))
        self.assertRedirects(response, detail_url)

    def test_split_sample_resolution_template(self):
        url = '/sample/split/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'split_sample')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/split_sample.html')

    def test_split_sample_content(self):
        url = reverse('split_sample')
        data = {'sample': 'xxxx'}
        response = self.client.get(url, data)
        self.assertContains(response, 'xxxx')

    def test_change_size_resolution_template(self):
        url = '/{0}/{1}/size/'.format(self.g1000, 1)
        match = resolve(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/sample_size.html')

    def test_split_sample_valid_data(self):
        obj = mommy.make(sample, growth=self.g1001, pocket=2)
        obj.parent = obj
        obj.save()
        url = reverse('split_sample')
        data = {'parent': 'g1001_2', 'pieces': 3}
        response = self.client.post(url, data)
        change_size_url = reverse('sample_change_size',
                                  args=(obj.growth.growth_number, obj.pocket))
        self.assertRedirects(response, change_size_url)

    def test_sample_size_valid_data(self):
        obj = mommy.make(sample, growth=self.g1001, pocket=2)
        obj.parent = obj
        obj.save()
        obj.split(3)
        url = reverse('sample_change_size',
                      args=(obj.growth.growth_number, obj.pocket))
        data = {'g1001_2a': 'whole', 'g1001_2b': 'half', 'g1001_2c': 'quarter'}
        response = self.client.post(url, data)
        detail_url = reverse('sample_family_detail',
                             args=(obj.growth.growth_number, obj.pocket))
        self.assertRedirects(response, detail_url)
        response = self.client.get(detail_url)
        for size in ['Whole', 'Half', 'Quarter']:
            self.assertContains(response, size)

    def test_readings_detail_resolution_template(self):
        url = '/{0}/readings/'.format(self.g1000)
        match = resolve(url)
        self.assertEqual(match.url_name, 'readings_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/readings_detail.html')

    def test_readings_detail_content(self):
        obj = mommy.make('growths.readings', growth=self.g1000,
                         layer_desc='test desc')
        url = reverse('readings_detail', args=(self.g1000,))
        response = self.client.get(url)
        self.assertContains(response, 'test desc')

    def test_readings_update_resolution_template(self):
        url = '/{0}/readings/update/'.format(self.g1000)
        match = resolve(url)
        self.assertEqual(match.url_name, 'update_readings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'growths/update_readings.html')

    def test_readings_update_content(self):
        obj = mommy.make('growths.readings', growth=self.g1000,
                         layer_desc='test desc')
        url = reverse('update_readings', args=(self.g1000,))
        response = self.client.get(url)
        self.assertContains(response, 'test desc')
