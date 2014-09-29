# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase


class TestHomepage(TestCase):

    def test_root_url_resolves_to_homepage(self):
        match = resolve('/')
        self.assertEqual(match.url_name, 'home')

    def test_homepage_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)
