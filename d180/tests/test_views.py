# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.forms import ValidationError
from django.test import TestCase

from model_mommy import mommy

from d180.models import D180Growth, Platter
from core.models import Investigation


class TestPlatterCRUD(TestCase):

    @classmethod
    def setUpClass(cls):
        get_user_model().objects.create_user('default', password='')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()

    def setUp(self):
        self.client.login(username='default', password='')

    def test_platter_list_resolution_template(self):
        url = '/d180/platters/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'platter_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'growths/platter_list.html')
        self.assertEqual(response.status_code, 200)


    def test_project_list_content(self):
        platters = [
            mommy.make(Platter),
            mommy.make(Platter),
            mommy.make(Platter),
            mommy.make(Platter),
        ]
        url = reverse('project_list')
        response = self.client.get(url)
        for platter in platters:
            self.assertContains(response, platter.serial)

    def test_platter_create_resolution_template(self):
        url = '/d180/platters/create/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'platter_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'growths/platter_create.html')
        self.assertEqual(response.status_code, 200)

    def test_platter_create_valid_data(self):
        url = reverse('platter_create')
        data = {
            'name': 'test platter',
            'serial': 'test-0001',
        }
        response = self.client.post(url, data)
        platter = Platter.objects.first()
        self.assertEqual(platter.serial, data['serial'])
        list_url = reverse('platter_list')
        self.assertRedirects(response, list_url)

    def test_platter_activate(self):
        platter = mommy.make(Platter, is_active=False)
        url = reverse('platter_activate', args=(platter.id,))
        list_url = reverse('platter_list')
        response = self.client.get(url)
        platter = Platter.objects.get(id=platter.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(platter.is_active)

    def test_platter_deactivate(self):
        platter = mommy.make(Platter, is_active=True)
        url = reverse('platter_deactivate', args=(platter.id,))
        list_url = reverse('platter_list')
        response = self.client.get(url)
        platter = Platter.objects.get(id=platter.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(platter.is_active)


class TestD180Wizard(TestCase):

    @classmethod
    def setUpClass(cls):
        get_user_model().objects.create_user('default', password='')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()

    def setUp(self):
        self.client.login(username='default', password='')

    def test_start_resolution_template(self):
        url = '/d180/growth/create/start/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_start')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'growths/create_growth_start.html')
        self.assertEqual(response.status_code, 200)

    def test_readings_resolution_template(self):
        mommy.make(D180Growth)
        url = '/d180/growth/create/readings/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_readings')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'growths/create_growth_readings.html')
        self.assertEqual(response.status_code, 200)

    def test_start_empty_data(self):
        """
        Test a post where no data is sent.
        """
        url = reverse('create_growth_d180_start')
        with self.assertRaises(ValidationError) as cm:
            self.client.post(url, {})
        exception = cm.exception
        self.assertEqual(exception.message,
            'ManagementForm data is missing or has been tampered with')

    def test_start_management_only(self):
        """
        Test a post where only managementform data is passed.
        """
        url = reverse('create_growth_d180_start')
        data = {
            'sample-INITIAL_FORMS': '0',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '1',
        }
        response = self.client.post(url, data)
        self.assertFormError(response, 'info_form', 'user',
            'This field is required.')
        self.assertFormError(response, 'growth_form', None,
            'At least one material must be specified')
        self.assertFormError(response, 'checklist_form', 'field_0',
            'This field is required.')
        self.assertFormError(response, 'source_form', 'cp2mg',
            'This field is required.')
        self.assertFormsetError(response, 'sample_formset', 0, None,
            'Cannot leave all fields blank.')

    def test_start_sample_formset_mixed_valid(self):
        """
        Test a post where one sample form is valid and one is not.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        url = reverse('create_growth_d180_start')
        data = {
            'sample-INITIAL_FORMS': '0',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '2',
            'checklist-field_0': 'on',
            'checklist-field_1': 'on',
            'checklist-field_2': 'on',
            'checklist-field_3': 'on',
            'checklist-field_4': 'on',
            'checklist-field_5': 'on',
            'checklist-field_6': 'on',
            'checklist-field_7': 'on',
            'checklist-field_8': 'on',
            'checklist-field_9': 'on',
            'checklist-field_10': 'on',
            'checklist-field_11': 'on',
            'checklist-field_12': 'on',
            'checklist-field_13': 'on',
            'growth-has_gan': 'on',
            'growth-has_u': 'on',
            'growth-orientation': '0001',
            'growth-investigations': '1',
            'growth-platter': '1',
            'growth-user': '1',
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
            'sample-0-substrate_comment': 'test',
            'sample-1-sample_uuid': 's0000',
        }
        response = self.client.post(url, data)
        self.assertFormsetError(response, 'sample_formset', 1, 'sample_uuid',
            'Sample s0000 not found')

    def test_start_valid(self):
        """
        Test a post where the form is valid.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        url = reverse('create_growth_d180_start')
        data = {
            'sample-INITIAL_FORMS': '1',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '1',
            'checklist-field_0': 'on',
            'checklist-field_1': 'on',
            'checklist-field_2': 'on',
            'checklist-field_3': 'on',
            'checklist-field_4': 'on',
            'checklist-field_5': 'on',
            'checklist-field_6': 'on',
            'checklist-field_7': 'on',
            'checklist-field_8': 'on',
            'checklist-field_9': 'on',
            'checklist-field_10': 'on',
            'checklist-field_11': 'on',
            'checklist-field_12': 'on',
            'checklist-field_13': 'on',
            'growth-has_gan': 'on',
            'growth-has_u': 'on',
            'growth-orientation': '0001',
            'growth-investigations': '1',
            'growth-platter': '1',
            'growth-user': '1',
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
            'sample-0-substrate_comment': 'test',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))
