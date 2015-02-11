# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import Process, ProcessNode, Sample, SplitProcess, Substrate
from .models import ChildProcess, ParentProcess


class TestProcessAPI(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
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


class TestSampleAPI(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        samples = [Sample.objects.create(substrate=mommy.make(Substrate))
                   for i in range(5)]
        response = self.client.get('/api/v0/sample/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('count'), len(samples))
        for sample, result in zip(samples, results.get('results')):
            self.assertEqual(result.get('uuid'), sample.uuid)

    def test_retrieve_view_get(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        response = self.client.get('/api/v0/sample/{}/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('uuid'), sample.uuid)

    def test_retrieve_view_tree(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        processes = {
            'step-1': [
                mommy.make(Process),
                mommy.make(Process),
            ],
            'step-2': [
                mommy.make(Process),
                mommy.make(Process),
                mommy.make(Process),
            ],
        }
        for process in processes['step-1']:
            sample.run_process(process)
        sample.split(3)
        for piece, process in zip(['a', 'b', 'c'], processes['step-2']):
            sample.run_process(process, piece)

        response = self.client.get('/api/v0/sample/{}/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        children = results.get('process_tree').get('children')
        self.assertEqual(len(children), 1)
        child = children[0]
        self.assertEqual(child.get('uuid'), processes['step-1'][0].uuid)
        self.assertEqual(len(child.get('children')), 1)
        child = child.get('children')[0]
        self.assertEqual(child.get('uuid'), processes['step-1'][1].uuid)
        self.assertEqual(len(child.get('children')), 3)
        for c, process, piece in zip(child.get('children'),
                                     processes['step-2'],
                                     ['a', 'b', 'c']):
            self.assertEqual(c.get('piece'), piece)
            self.assertEqual(len(c.get('children')), 1)
            self.assertEqual(c.get('children')[0].get('uuid'), process.uuid)

    def test_retrieve_view_leaf(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        processes = {
            'step-1': [
                mommy.make(Process),
                mommy.make(Process),
            ],
            'step-2': [
                mommy.make(Process),
                mommy.make(Process),
                mommy.make(Process),
            ],
        }
        for process in processes['step-1']:
            sample.run_process(process)
        sample.split(3)
        for piece, process in zip(['a', 'b', 'c'], processes['step-2']):
            sample.run_process(process, piece)

        response = self.client.get('/api/v0/sample/{}/leaf/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        leaf_nodes = results.get('leaf_nodes')
        leaf_uuids = [p.uuid for p in processes['step-2']]
        for node in leaf_nodes:
            self.assertIn(node.get('uuid'), leaf_uuids)


class TestUserAPI(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        response = self.client.get('/api/v0/users/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(results.get('count'), 1)
        user = results.get('results')[0]
        self.assertIsNotNone(user)
        self.assertEqual(user.get('username'), 'username1')
