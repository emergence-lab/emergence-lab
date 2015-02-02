from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth import get_user_model
from django.conf import settings

import aws_support as aws

from simulations.urls import urlpatterns


class TestSimulationViews(TestCase):

    def setUp(self):
        self.user_obj = get_user_model().objects.create_user('default', password='')
        self.client.login(username='default', password='')

    def test_instance_list(self):
        """
        Tests basic view.
        """
        url = reverse('simulation_admin')
        match = resolve('/simulations/')
        response = self.client.get(url)
        self.assertEqual(match.url_name, 'simulation_admin')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulations/admin.html')

    def test_ec2_connection(self):
        """
        Tests boto connection. Instance list should not be empty.
        Instance list should contain the base instance t2.micro
        """
        signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                    settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        self.assertNotEqual(signals.instance_list(), [])
        self.assertIn('t2.micro', [x.instance_type for x in signals.instance_list()])
