# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import re

from django.core.urlresolvers import reverse
from django.test import TestCase

from project_management.templatetags.dashboard_tags import (
    create_process_link,
    create_sample_link,
    create_literature_link,
)


class TestDashboardTags(TestCase):

    def test_create_sample_link_valid(self):
        sample = 's0001'
        html = re.sub(r"#\w+", create_sample_link, '#{}'.format(sample))
        self.assertEqual(html, '<a href="/samples/{0}/">{0}</a>'.format(sample))

    def test_create_sample_link_invalid(self):
        sample = 'invalid'
        html = re.sub(r"#\w+", create_sample_link, '#{}'.format(sample))
        self.assertEqual(html, '<a href="#">{0}</a>'.format(sample))

    def test_create_sample_link_invalid_no_pound(self):
        sample = 'invalid'
        html = re.sub(r"\w+", create_sample_link, sample)
        self.assertEqual(html, '<a href="#">{0}</a>'.format(sample))

    def test_create_process_link_valid(self):
        sample = 'p1234567'
        html = re.sub(r"#\w+", create_process_link, '#{}'.format(sample))
        self.assertEqual(html, '<a href="/process/{0}/">{0}</a>'.format(sample))

    def test_create_process_link_invalid(self):
        sample = 'invalid'
        html = re.sub(r"#\w+", create_process_link, '#{}'.format(sample))
        self.assertEqual(html, '<a href="#">{0}</a>'.format(sample))

    def test_create_process_link_invalid_no_pound(self):
        sample = 'invalid'
        html = re.sub(r"\w+", create_process_link, sample)
        self.assertEqual(html, '<a href="#">{0}</a>'.format(sample))
