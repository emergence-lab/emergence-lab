from django.test import TestCase
from django.contrib.auth.models import User

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from schedule_queue.models import Tool, Platter, Reservation

class TestTool(TestCase):
    
    def test_tool_str(self):
        tool_name = 'test_tool'
        obj = mommy.prepare(Tool, tool_name=tool_name)
        self.assertEqual(obj.__str__(), tool_name)
        
class TestPlatter(TestCase):
    
    def test_platter_str(self):
        platter_name = 'test_platter'
        obj = mommy.prepare(Platter, platter_name=platter_name)
        self.assertEqual(obj.__str__(), platter_name)
        
class TestReservation(TestCase):
    
    def test_reservation_str(self):
        tool_obj = mommy.make(Tool, tool_name='test_tool')
        user_obj = mommy.make(User, username='test_user')
        obj = mommy.prepare(Reservation, tool=tool_obj, user=user_obj, growth_length_in_hours=5)
        self.assertEqual(obj.__str__(), 'test_tool, test_user, 5')