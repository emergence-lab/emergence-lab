# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import Project, ProjectTracking, Investigation, Milestone


class TestProjectAPI(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        """
        Test that the list api returns correct items .
        """
        projects = [
            mommy.make(Project, name='project 1', slug='project-1', is_active=True),
            mommy.make(Project, name='project 2', slug='project-2', is_active=False),
        ]
        for project in projects:
            project.add_user(self.user, 'viewer')
        response = self.client.get('/api/v0/project_management/project/all')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), len(projects))
        for project, result in zip(projects, results):
            self.assertEqual(result['slug'], project.slug)

    def test_list_view_followed_get(self):
        """
        Test that the followed list api returns correct items .
        """
        projects = [
            mommy.make(Project, name='project 1', slug='project-1', is_active=True),
            mommy.make(Project, name='project 2', slug='project-2', is_active=False),
            mommy.make(Project, name='project 3', slug='project-3', is_active=True),
            mommy.make(Project, name='project 4', slug='project-4', is_active=False),
        ]
        # user is viewer on all projects
        for project in projects:
            project.add_user(self.user, 'viewer')
        # but is only tracking first two
        ProjectTracking.objects.get_or_create(project=projects[0], user=self.user)
        ProjectTracking.objects.get_or_create(project=projects[1], user=self.user)

        response = self.client.get('/api/v0/project_management/project/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), 2)
        for project, result in zip(projects[:2], results):
            self.assertEqual(result['slug'], project.slug)

    def test_retrieve_view_get(self):
        """
        Test retrieval of a project.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        project.add_user(self.user, 'viewer')
        response = self.client.get(
            '/api/v0/project_management/project/detail/{}'.format(project.slug))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('slug'), project.slug)
        self.assertIsNotNone(results.get('description'))

    def test_create_view(self):
        """
        Test creation of a project using the API.
        """
        url = '/api/v0/project_management/project/'
        data = {'name': 'project 1', 'description': 'Test description'}
        response = self.client.post(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        project = Project.objects.first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(project.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])
        self.assertTrue(project in self.user.get_projects('viewer'))

    def test_update_view(self):
        """
        Test update of a project using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        project.add_user(self.user, 'owner')
        url = '/api/v0/project_management/project/edit/{}'.format(project.slug)
        data = {'name': 'project 1',
                'description': 'Test updated description',
                'is_active': 'true'}
        response = self.client.patch(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        project = Project.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])

    def test_track_view(self):
        """
        Test tracking of a project using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        project.add_user(self.user, 'viewer')
        self.assertFalse(project in self.user.get_projects('viewer', followed=True))
        url = '/api/v0/project_management/project/track/{}'.format(project.slug)
        response = self.client.get(url)
        self.assertTrue(project in self.user.get_projects('viewer', followed=True))

    def test_untrack_view(self):
        """
        Test tracking of a project using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        project.add_user(self.user, 'viewer')
        ProjectTracking.objects.get_or_create(project=project, user=self.user)
        self.assertTrue(project in self.user.get_projects('viewer', followed=True))
        url = '/api/v0/project_management/project/untrack/{}'.format(project.slug)
        response = self.client.get(url)
        self.assertFalse(project in self.user.get_projects('viewer', followed=True))


class TestInvestigationAPI(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        """
        Test that the list api returns correct items .
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigations = [
            mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                       project=project, is_active=True),
            mommy.make(Investigation, name='investigation 2', slug='investigation-2',
                       project=project, is_active=False),
        ]
        project.add_user(self.user, 'viewer')
        response = self.client.get('/api/v0/project_management/investigation/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), len(investigations))
        for investigation, result in zip(investigations, results):
            self.assertEqual(result['slug'], investigation.slug)

    def test_bad_create_view(self):
        """
        Test unauthorized creation of an investigation using the API errors to 403 Forbidden.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        url = '/api/v0/project_management/investigation/'
        data = {'name': 'investigation 1',
                'description': 'Test description',
                'project': project.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(project.is_owner(self.user))

    def test_retrieve_view_get(self):
        """
        Test retrieval of an investigation.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   project=project, is_active=True)
        project.add_user(self.user, 'viewer')
        response = self.client.get(
            '/api/v0/project_management/investigation/detail/{}'.format(investigation.slug))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('slug'), investigation.slug)
        self.assertIsNotNone(results.get('description'))

    def test_create_view(self):
        """
        Test creation of an investigation using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        project.add_user(self.user, 'owner')
        url = '/api/v0/project_management/investigation/'
        data = {'name': 'investigation 1',
                'description': 'Test description',
                'project': project.id}
        response = self.client.post(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        investigation = Investigation.objects.first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(investigation.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])
        self.assertTrue(investigation in self.user.get_investigations('viewer'))

    def test_update_view(self):
        """
        Test update of an investigation using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   is_active=True, project=project)
        project.add_user(self.user, 'owner')
        url = '/api/v0/project_management/investigation/edit/{}'.format(investigation.slug)
        data = {'name': 'investigation 1',
                'description': 'Test description',
                'project': project.id,
                'is_active': 'true'}
        response = self.client.patch(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        investigation = Investigation.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(investigation.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])


class TestMilestoneAPI(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client = APIClient()
        self.client.login(username='username1', password='')

    def test_list_view_get(self):
        """
        Test that the list api returns correct items .
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   project=project, is_active=True)
        milestones = [
            mommy.make(Milestone, name='milestone 1', slug='milestone-1',
                       investigation=investigation, is_active=True),
            mommy.make(Milestone, name='milestone 2', slug='milestone-2',
                       investigation=investigation, is_active=True),
        ]
        project.add_user(self.user, 'viewer')
        response = self.client.get('/api/v0/project_management/milestone/')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(results), len(milestones))
        for milestone, result in zip(milestones, results):
            self.assertEqual(result['slug'], milestone.slug)

    def test_retrieve_view_get(self):
        """
        Test retrieval of a milestone.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   project=project, is_active=True)
        milestone = mommy.make(Milestone, name='milestone 1', slug='milestone-1',
                               investigation=investigation, is_active=True)
        project.add_user(self.user, 'viewer')
        response = self.client.get(
            '/api/v0/project_management/milestone/detail/{}'.format(milestone.slug))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertEqual(results.get('slug'), milestone.slug)
        self.assertIsNotNone(results.get('description'))

    def test_create_view(self):
        """
        Test creation of a milestone using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   project=project, is_active=True)
        project.add_user(self.user, 'owner')
        url = '/api/v0/project_management/milestone/'
        data = {'name': 'milestone 1',
                'description': 'Test description',
                'investigation': investigation.id,
                'due_date': str(datetime.date.today())}
        response = self.client.post(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        milestone = Milestone.objects.first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(milestone.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])
        self.assertTrue(milestone in self.user.get_milestones('viewer'))

    def test_bad_create_view(self):
        """
        Test unauthorized creation of a milestone using the API errors to 403 Forbidden.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   project=project, is_active=True)
        url = '/api/v0/project_management/milestone/'
        data = {'name': 'milestone 1',
                'description': 'Test description',
                'investigation': investigation.id,
                'due_date': str(datetime.date.today())}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(project.is_owner(self.user))

    def test_update_view(self):
        """
        Test update of a milestone using the API.
        """
        project = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        investigation = mommy.make(Investigation, name='investigation 1', slug='investigation-1',
                                   is_active=True, project=project)
        milestone = mommy.make(Milestone, name='milestone 1', slug='milestone-1',
                               investigation=investigation, is_active=True)
        project.add_user(self.user, 'owner')
        url = '/api/v0/project_management/milestone/edit/{}'.format(milestone.slug)
        data = {'name': 'milestone 1',
                'description': 'Test description',
                'investigation': investigation.id,
                'due_date': str(datetime.date.today())}
        response = self.client.patch(url, data, format='json')
        results = json.loads(response.content.decode('utf-8'))
        milestone = Milestone.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(milestone.description, data['description'])
        self.assertEqual(results.get('description'), data['description'])
