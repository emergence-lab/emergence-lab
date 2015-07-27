from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from schedule_queue.models import Reservation


class TestReservation(TestCase):
    pass
