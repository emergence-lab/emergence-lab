# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.forms import ValidationError
from django.test import TestCase

from model_mommy import mommy

from d180.models import D180Growth, D180Readings, Platter
from core.models import Investigation, Sample, ProcessNode


class TestPlatterCRUD(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_platter_list_resolution_template(self):
        url = '/d180/platters/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'platter_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'd180/platter_list.html')
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
        self.assertTemplateUsed(response, 'd180/platter_create.html')
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

    def setUp(self):
        self.user = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_start_resolution_template(self):
        url = '/d180/growth/create/start/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_start')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'd180/create_growth_start.html')
        self.assertEqual(response.status_code, 200)

    def test_readings_resolution_template(self):
        mommy.make(D180Growth)
        url = '/d180/growth/create/readings/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_readings')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'd180/create_growth_readings.html')
        self.assertEqual(response.status_code, 200)

    def test_postrun_resolution_template(self):
        mommy.make(D180Growth)
        url = '/d180/growth/create/postrun/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_postrun')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'd180/create_growth_postrun.html')
        self.assertEqual(response.status_code, 200)

    def test_cancel(self):
        # check url resolution
        url = '/d180/growth/create/cancel/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'create_growth_d180_cancel')

        # set up objects
        investigation = mommy.make(Investigation)
        growth = mommy.make(D180Growth)
        growth.investigations.add(investigation)
        readings = mommy.make(D180Readings, growth=growth)
        sample = Sample.objects.create(substrate=mommy.make('Substrate'))
        sample.run_process(growth)
        nodes = growth.processnode_set.all()
        self.assertListEqual(list(sample.get_nodes_for_process_type(D180Growth)),
                             list(nodes))

        # check url resolution
        response = self.client.get(url)
        self.assertRedirects(response, reverse('dashboard'))

        # refresh objects from db, some no longer exist
        investigation = Investigation.objects.get(pk=investigation.pk)
        sample = Sample.objects.get(pk=sample.pk)
        nodes = ProcessNode.objects.filter(pk__in=[n.pk for n in nodes])

        # growth no longer exists
        with self.assertRaises(D180Growth.DoesNotExist):
            growth = D180Growth.objects.get(pk=growth.pk)

        # readings no longer exists
        with self.assertRaises(D180Readings.DoesNotExist):
            readings = D180Readings.objects.get(pk=readings.pk)

        # process node no longer exists
        self.assertListEqual([], list(nodes))
        self.assertListEqual([],
                             list(sample.get_nodes_for_process_type(D180Growth)))

        # many-to-many relationship with investigation no longer exists
        self.assertListEqual([], list(investigation.growths.all()))

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
            'Cannot leave all substrate fields blank.')

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
            'growth-user': self.user.id,
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

    def test_start_valid_new_sample(self):
        """
        Test a post where the form is valid, creating a new sample.
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
            'growth-user': self.user.id,
            'growth-legacy_identifier': 'g2000',
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
        node = ProcessNode.objects.last()
        self.assertEqual(node.number, 1)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))

    def test_start_valid_existing_sample(self):
        """
        Test a post where the form is valid, using an existing sample.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        sample = Sample.objects.create(substrate=mommy.make('Substrate'))
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
            'growth-user': self.user.id,
            'growth-legacy_identifier': 'g2000',
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
            'sample-0-sample_uuid': sample.uuid,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))

    def test_start_valid_existing_sample_piece(self):
        """
        Test a post where the form is valid, using an existing sample specifying
        the piece.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        sample = Sample.objects.create(substrate=mommy.make('Substrate'))
        sample.split(self.user, 2)
        piece = 'b'
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
            'growth-user': self.user.id,
            'growth-legacy_identifier': 'g2000',
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
            'sample-0-sample_uuid': '{}{}'.format(sample.uuid, piece),
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))
        nodes = sample.get_nodes_for_process_type(D180Growth)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].piece, piece)

    def test_start_ambiguous_sample(self):
        """
        Test a post where the specified sample is ambiguous.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        sample = Sample.objects.create(substrate=mommy.make('Substrate'))
        sample.split(self.user, 2)
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
            'growth-user': self.user.id,
            'growth-legacy_identifier': 'g2000',
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
            'sample-0-sample_uuid': '{}'.format(sample.uuid),
        }
        response = self.client.post(url, data)
        self.assertFormsetError(response, 'sample_formset', 0, 'sample_uuid',
            'Sample {} is ambiguous, piece needs to be specified'.format(sample.uuid))

    def test_start_valid_hold_reservation(self):
        """
        Test a post where the form is valid, selecting to hold the reservation.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        user = get_user_model().objects.first()
        reservation = mommy.make('schedule_queue.Reservation',
                                 user=user, is_active=True, tool='d180')
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
            'growth-user': self.user.id,
            'growth-legacy_identifier': 'g2000',
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
            'reservation-hold_open': 'on',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))
        reservation = type(reservation).objects.get(id=reservation.id)
        self.assertTrue(reservation.is_active)

    def test_start_valid_close_reservation(self):
        """
        Test a post where the form is valid, without holding the reservation.
        """
        mommy.make(Investigation)
        mommy.make(Platter)
        user = get_user_model().objects.first()
        reservation = mommy.make('schedule_queue.Reservation',
                                 user=user, is_active=True, tool='d180')
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
            'growth-legacy_identifier': 'g2000',
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
        reservation = type(reservation).objects.get(id=reservation.id)
        self.assertFalse(reservation.is_active)

    def test_readings_empty_data(self):
        """
        Test a post where no data is sent.
        """
        mommy.make(D180Growth)
        url = reverse('create_growth_d180_readings')
        with self.assertRaises(ValidationError) as cm:
            self.client.post(url, {})
        exception = cm.exception
        self.assertEqual(exception.message,
            'ManagementForm data is missing or has been tampered with')

    def test_readings_management_only(self):
        """
        Test a post where only managementform data is passed.
        """
        mommy.make(D180Growth)
        url = reverse('create_growth_d180_readings')
        data = {
            'reading-INITIAL_FORMS': '0',
            'reading-MAX_NUM_FORMS': '',
            'reading-TOTAL_FORMS': '1',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))

    def test_readings_readings_formset_invalid(self):
        mommy.make(D180Growth)
        url = reverse('create_growth_d180_readings')
        data = {
            'reading-INITIAL_FORMS': '0',
            'reading-MAX_NUM_FORMS': '',
            'reading-TOTAL_FORMS': '1',
            'reading-0-layer_desc': 'test',
        }
        response = self.client.post(url, data)
        self.assertFormsetError(response, 'readings_formset', 0, 'layer',
            'This field is required.')

    def test_readings_readings_formset_valid(self):
        growth = mommy.make(D180Growth)
        url = reverse('create_growth_d180_readings')
        data = {
            'reading-INITIAL_FORMS': '0',
            'reading-MAX_NUM_FORMS': '',
            'reading-TOTAL_FORMS': '1',
            'reading-0-alkyl_flow_inner': '0.0',
            'reading-0-alkyl_flow_middle': '0.0',
            'reading-0-alkyl_flow_outer': '0.0',
            'reading-0-alkyl_push_inner': '0.0',
            'reading-0-alkyl_push_middle': '0.0',
            'reading-0-alkyl_push_outer': '0.0',
            'reading-0-cp2mg_dilution': '0.0',
            'reading-0-cp2mg_flow': '0.0',
            'reading-0-cp2mg_pressure': '0.0',
            'reading-0-current_in': '0.0',
            'reading-0-current_out': '0.0',
            'reading-0-ecp_temp': '0.0',
            'reading-0-gc_position': '0.0',
            'reading-0-gc_pressure': '0.0',
            'reading-0-h2_flow': '0.0',
            'reading-0-hydride_inner': '0.0',
            'reading-0-hydride_outer': '0.0',
            'reading-0-hydride_pressure': '0.0',
            'reading-0-layer': '1',
            'reading-0-layer_desc': 'test',
            'reading-0-motor_rpm': '0.0',
            'reading-0-n2_flow': '0.0',
            'reading-0-nh3_flow': '0.0',
            'reading-0-pyro_in': '0.0',
            'reading-0-pyro_out': '0.0',
            'reading-0-silane_dilution': '0.0',
            'reading-0-silane_flow': '0.0',
            'reading-0-silane_mix': '0.0',
            'reading-0-silane_pressure': '0.0',
            'reading-0-tc_in': '0.0',
            'reading-0-tc_out': '0.0',
            'reading-0-tega2_flow': '0.0',
            'reading-0-tega2_pressure': '0.0',
            'reading-0-tmal1_flow': '0.0',
            'reading-0-tmal1_pressure': '0.0',
            'reading-0-tmga1_flow': '0.0',
            'reading-0-tmga1_pressure': '0.0',
            'reading-0-tmga2_flow': '0.0',
            'reading-0-tmga2_pressure': '0.0',
            'reading-0-tmin1_flow': '0.0',
            'reading-0-tmin1_pressure': '0.0',
            'reading-0-top_vp_flow': '0.0',
            'reading-0-voltage_in': '0.0',
            'reading-0-voltage_out': '0.0',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('create_growth_d180_readings'))
        self.assertEqual(growth.readings.count(), 1)
        self.assertEqual(growth.readings.first().layer_desc, 'test')

    def test_postrun_empty_data(self):
        """
        Test a post where no data is sent.
        """
        mommy.make(D180Growth)
        url = reverse('create_growth_d180_postrun')
        response = self.client.post(url, {})
        self.assertFormError(response, 'source_form', 'cp2mg',
            'This field is required.')
        self.assertFormError(response, 'checklist_form', 'field_0',
            'This field is required.')

    def test_postrun_valid(self):
        process = mommy.make(D180Growth)
        url = reverse('create_growth_d180_postrun')
        data = {
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
            'source-cp2mg': '0.00',
            'source-nh3': '0.00',
            'source-sih4': '0.00',
            'source-tega1': '0.00',
            'source-tmal1': '0.00',
            'source-tmga1': '0.00',
            'source-tmga2': '0.00',
            'source-tmin1': '0.00',
            'source-tmin2': '0.00',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('process_detail', args=(process.uuid,)))
