# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from model_mommy import mommy

from core.models import ProcessType
from core.tests.helpers import test_resolution_template
from d180.models import Platter
from schedule_queue.models import Reservation


class TestReservationCRUD(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_reservation_edit_resolution_template(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservation = mommy.make(Reservation,
                                 tool=process_type,
                                 user=self.user)
        test_resolution_template(self,
            url='/scheduling/edit/{}/'.format(reservation.id),
            url_name='reservation_edit',
            template_file='schedule_queue/reservation_edit.html')

    def test_reservation_create_resolution_template(self):
        test_resolution_template(self,
            url='/scheduling/create/',
            url_name='reservation_create',
            template_file='schedule_queue/reservation_form.html')

    def test_create_reservation_valid_data(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        url = reverse('reservation_create')
        data =  {
            'tool': process_type.type,
            'platter': mommy.make(Platter).id,
            'user': self.user,
            'growth_length': 6,
            'bake_length': 30,
            'priority': 10,
            'comment': 'testing'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('reservation_list', args=(process_type.type,)))
        self.assertEqual(Reservation.objects.first().comment, 'testing')

    def test_reservation_edit_valid_data(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservation = mommy.make(Reservation,
                             tool=process_type,
                             user=self.user)
        url = reverse('reservation_edit', kwargs={'pk': reservation.id})
        data = {
            'tool': process_type.type,
            'platter': reservation.platter_id,
            'user': reservation.user,
            'growth_length': 6,
            'bake_length': 30,
            'comment': 'testing',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('reservation_list', args=(process_type.type,)))
        self.assertEqual(Reservation.objects.first().comment, 'testing')

    def test_increase_priority_resolution(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=10),
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=20),
        ]
        match = resolve('/scheduling/increase/{}/'.format(reservations[-1].id))
        self.assertEqual(match.url_name, 'increase_priority')

    def test_decrease_priority_resolution(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=10),
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=20),
        ]
        match = resolve('/scheduling/decrease/{}/'.format(reservations[0].id))
        self.assertEqual(match.url_name, 'decrease_priority')

    def test_increase_priority(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=10, comment='a'),
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=20, comment='b'),
        ]
        url = reverse('increase_priority', kwargs={'pk': reservations[-1].id})
        response = self.client.get(url)
        reservations = [Reservation.objects.get(id=r.id) for r in reservations]
        self.assertEqual(reservations[0].priority, 20)
        self.assertEqual(reservations[1].priority, 10)

    def test_decrease_priority(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=10),
            mommy.make(Reservation, tool=process_type,
                       user=self.user, priority=20),
        ]
        url = reverse('decrease_priority', kwargs={'pk': reservations[0].id})
        response = self.client.get(url)
        reservations = [Reservation.objects.get(id=r.id) for r in reservations]
        self.assertEqual(reservations[0].priority, 20)
        self.assertEqual(reservations[1].priority, 10)

    def test_deactivate_reservation_resolution(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservation = mommy.make(Reservation,
                                 tool=process_type, user=self.user)
        match = resolve('/scheduling/cancel/{}/'.format(reservation.id))
        self.assertEqual(match.url_name, 'cancel_reservation')

    def test_deactivate_reservation(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        res_obj = mommy.make(Reservation,
                             tool=process_type,
                             user=self.user,
                             growth_length=5)
        match = resolve('/scheduling/cancel/{0}/'.format(res_obj.id))
        url = reverse('cancel_reservation', kwargs={'pk': res_obj.id})
        response = self.client.get(url)
        res_act_field = Reservation.objects.all().filter(user=self.user).first().is_active
        self.assertEqual(match.url_name, 'cancel_reservation')
        self.assertFalse(res_act_field, msg=None)

    def test_list_view(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type, user=self.user),
            mommy.make(Reservation, tool=process_type, user=self.user),
        ]
        url = reverse('reservation_list', kwargs={'process': process_type.type})
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']),
                         len(Reservation.objects.all().filter(tool=process_type)))

    def test_reservation_list_resolution_template(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type, user=self.user),
            mommy.make(Reservation, tool=process_type, user=self.user),
        ]
        test_resolution_template(self,
            url='/scheduling/list/{}/'.format(process_type.type),
            url_name='reservation_list',
            template_file='schedule_queue/reservation_list.html')

    def test_reservation_landing_resolution_template(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type, user=self.user, is_active=False),
            mommy.make(Reservation, tool=process_type, user=self.user),
        ]
        test_resolution_template(self,
            url='/scheduling/',
            url_name='reservation_landing',
            template_file='schedule_queue/reservation_landing.html')

    def test_reservation_landing_content(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type, user=self.user, is_active=False),
            mommy.make(Reservation, tool=process_type, user=self.user),
        ]
        url = reverse('reservation_landing')
        response = self.client.get(url)
        self.assertContains(response, process_type.name)

    def test_reservation_landing_count_open_only(self):
        process_type = mommy.make(
            ProcessType,
            type='test',
            configuration={'core_scheduling_type': 'simple'})
        reservations = [
            mommy.make(Reservation, tool=process_type, user=self.user, is_active=False),
            mommy.make(Reservation, tool=process_type, user=self.user),
        ]
        url = reverse('reservation_landing')
        response = self.client.get(url)
        open_reservations = next(ptype.open_reservations
                                 for ptype
                                 in response.context['object_list']
                                 if ptype.type == process_type.type)
        self.assertEqual(open_reservations, 1)
