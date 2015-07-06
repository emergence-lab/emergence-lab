from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

import schedule_queue.config as tools
from schedule_queue.models import Reservation


class TestReservation(TestCase):

    def test_reservation_str(self):
        tool_obj = tools.get_tool_list()[0]
        user_obj = get_user_model().objects.create_user('default', password='')
        obj = mommy.prepare(Reservation, tool=tool_obj, user=user_obj, growth_length=5)
        self.assertEqual(obj.__str__(), '{}, default, 5'.format(tools.get_tool_list()[0]))
