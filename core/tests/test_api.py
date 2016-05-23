# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import DataFile, Process, ProcessNode, Sample, Substrate


class TestProcessAPI(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        """
        Test that the list api returns correct items .
        """
        processes = [
            mommy.make(Process),
            mommy.make(Process),
        ]
        response = self.client.get('/api/v0/process/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), len(processes))
        for process, result in zip(processes, results):
            self.assertEqual(result.get('uuid_full'), str(process.uuid_full))

    def test_retrieve_view_get_full_uuid(self):
        """
        Test retrieval of a process using the full uuid.
        """
        process = mommy.make(Process)
        response = self.client.get(
            '/api/v0/process/{}/'.format(str(process.uuid_full)))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('uuid_full'), str(process.uuid_full))
        self.assertIsNotNone(results.get('comment'))

    def test_retrieve_view_get_short_uuid(self):
        """
        Test retrieval of a process using the short uuid.
        """
        process = mommy.make(Process)
        response = self.client.get(
            '/api/v0/process/{}/'.format(process.uuid))
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('uuid_full'), str(process.uuid_full))
        self.assertIsNotNone(results.get('comment'))

    def test_retrieve_node_view_get_full_uuid(self):
        """
        Test retrieval of a process node using the full uuid.
        """
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        sample.run_process(mommy.make(Process))
        node = sample.leaf_nodes[0]
        response = self.client.get(
            '/api/v0/process/node/{}/'.format(str(node.uuid_full)))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('uuid_full'), str(node.uuid_full))
        self.assertIsNotNone(results.get('comment'))
        self.assertEqual(results.get('sample'), sample.uuid)

    def test_retrieve_node_view_get_short_uuid(self):
        """
        Test retrieval of a process node using the short uuid.
        """
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        sample.run_process(mommy.make(Process))
        node = sample.leaf_nodes[0]
        response = self.client.get(
            '/api/v0/process/node/{}/'.format(node.uuid))
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('uuid_full'), str(node.uuid_full))
        self.assertIsNotNone(results.get('comment'))
        self.assertEqual(results.get('sample'), sample.uuid)

    def test_retrieve_file_view(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        process = mommy.make(Process)
        datafile = mommy.make(DataFile)
        process.datafiles.add(datafile)
        sample.run_process(process)
        response = self.client.get(
            '/api/v0/process/{}/files/'.format(process.uuid))
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0].get('id'))
        self.assertEqual(results[0].get('id'), datafile.id)


class TestSampleAPI(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        samples = [Sample.objects.create(substrate=mommy.make(Substrate))
                   for i in range(5)]
        response = self.client.get('/api/v0/sample/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), len(samples))
        for sample, result in zip(samples, results):
            self.assertEqual(result.get('uuid'), sample.uuid)

    def test_retrieve_view_get(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        response = self.client.get('/api/v0/sample/{}/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
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
        sample.split(self.user, 3)
        for piece, process in zip(['a', 'b', 'c'], processes['step-2']):
            sample.run_process(process, piece)

        response = self.client.get('/api/v0/sample/{}/node/tree/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))

        children = results.get('nodes').get('children')
        self.assertEqual(len(children), 1)
        child = children[0]
        self.assertEqual(child.get('process').get('uuid'),
                         processes['step-1'][0].uuid)
        self.assertEqual(len(child.get('children')), 1)
        child = child.get('children')[0]
        self.assertEqual(child.get('process').get('uuid'),
                         processes['step-1'][1].uuid)
        self.assertEqual(len(child.get('children')), 3)
        for c, process, piece in zip(child.get('children'),
                                     processes['step-2'],
                                     ['a', 'b', 'c']):
            self.assertEqual(c.get('piece'), piece)
            self.assertEqual(len(c.get('children')), 1)
            self.assertEqual(c.get('children')[0].get('process').get('uuid'),
                             process.uuid)

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
        sample.split(self.user, 3)
        for piece, process in zip(['a', 'b', 'c'], processes['step-2']):
            sample.run_process(process, piece)

        response = self.client.get('/api/v0/sample/{}/node/leaf/'.format(sample.uuid))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        leaf_nodes = results.get('nodes')
        leaf_uuids = [p.uuid for p in processes['step-2']]
        for node in leaf_nodes:
            self.assertIn(node.get('process').get('uuid'), leaf_uuids)


class TestUserAPI(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        response = self.client.get('/api/v0/users/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), 1)
        user = results[0]
        self.assertIsNotNone(user)
        self.assertEqual(user.get('username'), 'username1')
