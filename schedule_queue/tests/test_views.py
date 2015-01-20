from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.test.client import RequestFactory
from model_mommy import mommy
from schedule_queue.models import Reservation
from schedule_queue.views import ReservationLanding
from schedule_queue.urls import urlpatterns
from d180.models import Platter
import schedule_queue.config as tools
from django.contrib.auth import get_user_model
import time


class TestReservationCRUD(TestCase):

    def setUp(self):
        self.user_obj = get_user_model().objects.create_user('default', password='')
        self.platter_obj = Platter.objects.create(name='test_platter')
        self.tool_obj = tool_obj = tools.get_tool_list()[0]
        self.client.login(username='default', password='')

    def test_create_reservation(self):
        res_obj = mommy.make(Reservation,
                             tool=self.tool_obj,
                             user=self.user_obj,
                             growth_length_in_hours=5)
        res_id = Reservation.objects.all().filter(user=self.user_obj).first().id
        url = reverse('reservation_edit', kwargs={'pk': res_obj.id})
        match = resolve('/scheduling/edit/{0}/'.format(res_obj.id))
        response = self.client.get(url)
        self.assertEqual(match.url_name, 'reservation_edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_queue/reservation_edit.html')

    def test_create_reservation_form(self):
        url = reverse('reservation_create')
        match = resolve('/scheduling/new/')
        response = self.client.post(url, {'tool': self.tool_obj, 'platter': self.platter_obj,
                                          'user': self.user_obj, 'growth_length_in_hours': 6,
                                          'bake_length_in_minutes': 30,
                                          'priority_field': 10*time.time()})
        self.assertEqual(match.url_name, 'reservation_create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_queue/reservation_form.html')

    def test_edit_reservation_form(self):
        res_obj = mommy.make(Reservation,
                             tool=self.tool_obj,
                             user=self.user_obj,
                             growth_length_in_hours=5)
        url = reverse('reservation_edit', kwargs={'pk': res_obj.id})
        match = resolve('/scheduling/edit/{0}/'.format(res_obj.id))
        response = self.client.post(url, {'growth_length_in_hours': 6,
                                          'bake_length_in_minutes': 30})
        self.assertEqual(match.url_name, 'reservation_edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_queue/reservation_edit.html')

    def test_increase_priority(self):
        res_obj_1 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=5, priority_field=int(10*time.time()))
        res_obj_2 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=4, priority_field=int((10*time.time())+1))
        url = reverse('increase_priority',
                      kwargs={'pk': res_obj_2.id})
        match = resolve('/scheduling/increase/{0}/'.format(res_obj_2.id))
        response = self.client.get(url)
        res_list = Reservation.objects.all().filter(
            priority_field__lte=int((10*time.time())+2)).order_by('-priority_field')
        self.assertEqual(match.url_name, 'increase_priority')
        self.assertTrue(res_list[1].priority_field < res_list[0].priority_field, msg=None)

    def test_decrease_priority(self):
        res_obj_1 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=5, priority_field=int(10*time.time()))
        res_obj_2 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=4, priority_field=int((10*time.time())+1))
        url = reverse('decrease_priority',
                      kwargs={'pk': res_obj_1.id})
        match = resolve('/scheduling/decrease/{0}/'.format(res_obj_1.id))
        response = self.client.get(url)
        res_list = Reservation.objects.all().filter(
            priority_field__lte=int((10*time.time())+2)).order_by('-priority_field')
        self.assertEqual(match.url_name, 'decrease_priority')
        self.assertTrue(res_list[1].priority_field < res_list[0].priority_field, msg=None)

    def test_deactivate_reservation(self):
        res_obj = mommy.make(Reservation,
                             tool=self.tool_obj,
                             user=self.user_obj,
                             growth_length_in_hours=5)
        match = resolve('/scheduling/cancel/{0}/'.format(res_obj.id))
        url = reverse('cancel_reservation', kwargs={'pk': res_obj.id})
        response = self.client.get(url)
        res_act_field = Reservation.objects.all().filter(user=self.user_obj).first().is_active
        self.assertEqual(match.url_name, 'cancel_reservation')
        self.assertFalse(res_act_field, msg=None)

    def test_list_view(self):
        res_obj_1 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=5,
                               priority_field=int(10*time.time()))
        res_obj_2 = mommy.make(Reservation,
                               tool=self.tool_obj,
                               user=self.user_obj,
                               growth_length_in_hours=4,
                               priority_field=int((10*time.time())+1))
        match = resolve('/scheduling/{0}/'.format(self.tool_obj))
        url = reverse('reservation_list_by_tool', kwargs={'tool_slug': self.tool_obj})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_queue/reservation_list.html')
        self.assertEqual(len(response.context['object_list']),
                         len(Reservation.objects.all().filter(tool=self.tool_obj)))
        self.assertEqual(match.url_name, 'reservation_list_by_tool')
