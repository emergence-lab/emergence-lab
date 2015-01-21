# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import Process, ProcessNode, Sample, SplitProcess
from .models import ChildProcess, ParentProcess


class TestProcessAPI(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        user1 = User.objects.create_user('username1', password='')

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get_homogeneous(self):
        """
        Test that the list api returns correct items if they are all the same
        process class.
        """
        processes = [
            mommy.make(Process),
            mommy.make(Process),
        ]
        response = self.client.get('/api/v0/process/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('count'), len(processes))
        for process, result in zip(processes, results.get('results')):
            self.assertEqual(result.get('uuid_full'), process.uuid_full.hex)

    def test_list_view_get_heterogeneous(self):
        """
        Test that the list api returns correct items if they are different
        process classes without polymorphic fields.
        """
        processes = [
            mommy.make(Process),
            mommy.make(SplitProcess),
        ]
        response = self.client.get('/api/v0/process/')
        results = json.loads(response.content)
        self.assertEqual(results.get('count'), len(processes))
        for process, result in zip(processes, results.get('results')):
            self.assertEqual(result.get('uuid_full'), process.uuid_full.hex)

    def test_list_view_get_polymorphic(self):
        """
        Test that the list api returns correct items if they are different
        models that provide polymorphic fields.
        """
        processes = [
            mommy.make(Process),
            mommy.make(SplitProcess),
            mommy.make(ParentProcess),
            mommy.make(ChildProcess),
        ]
        response = self.client.get('/api/v0/process/')
        results = json.loads(response.content)
        self.assertEqual(results.get('count'), len(processes))
        for process, result in zip(processes, results.get('results')):
            self.assertEqual(result.get('uuid_full'), process.uuid_full.hex)
            self.assertIsNotNone(result.get('comment'))
            polymorphic_ctype = result.get('polymorphic_ctype')
            if polymorphic_ctype == 'ParentProcess':
                self.assertIsNotNone(result.get('parent_field'))
            elif polymorphic_ctype == 'ChildProcess':
                self.assertIsNotNone(result.get('parent_field'))
                self.assertIsNotNone(result.get('child_field'))

    def test_retrieve_view_get_full_uuid(self):
        """
        Test retrieval of a process using the full uuid.
        """
        process = mommy.make(ChildProcess)
        response = self.client.get(
            '/api/v0/process/{}/'.format(process.uuid_full.hex))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('uuid_full'), process.uuid_full.hex)
        self.assertIsNotNone(results.get('comment'))

    def test_retrieve_view_get_short_uuid(self):
        """
        Test retrieval of a process using the short uuid.
        """
        process = mommy.make(ChildProcess)
        response = self.client.get(
            '/api/v0/process/{}/'.format(process.uuid))
        results = json.loads(response.content)
        self.assertEqual(results.get('uuid_full'), process.uuid_full.hex)
        self.assertIsNotNone(results.get('comment'))

    def test_retrieve_node_view_get_full_uuid(self):
        """
        Test retrieval of a process node using the full uuid.
        """
        node = mommy.make(ProcessNode)
        response = self.client.get(
            '/api/v0/process/node/{}/'.format(node.uuid_full.hex))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('uuid_full'), node.uuid_full.hex)
        self.assertIsNotNone(results.get('comment'))

    def test_retrieve_node_view_get_short_uuid(self):
        """
        Test retrieval of a process node using the short uuid.
        """
        node = mommy.make(ProcessNode)
        response = self.client.get(
            '/api/v0/process/node/{}/'.format(node.uuid))
        results = json.loads(response.content)
        self.assertEqual(results.get('uuid_full'), node.uuid_full.hex)
        self.assertIsNotNone(results.get('comment'))
