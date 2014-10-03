# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from model_mommy import mommy

from core.models import Investigation, operator, Project, project_tracking


class TestHomepage(TestCase):

    @classmethod
    def setUpClass(cls):
        get_user_model().objects.create_user('default', password='')

    def test_homepage_url_resolution(self):
        match = resolve('/')
        self.assertEqual(match.url_name, 'home')

    def test_homepage_access_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)

    def test_homepage_access_login(self):
        result = self.client.login(username='default', password='')
        self.assertTrue(result)

        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)


class TestOperatorCRUD(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        user1 = User.objects.create_user('username1', password='')
        user2 = User.objects.create_user('username2', password='')
        operator.objects.create(name='name 1', user=user1,
                                is_active=True)
        operator.objects.create(name='name 2', user=user2,
                                is_active=False)

    @classmethod
    def tearDownClass(cls):
        operator.objects.all().delete()
        get_user_model().objects.all().delete()

    def setUp(self):
        self.client.login(username='username1', password='')

    def test_operator_list_url_resolution(self):
        match = resolve('/operators/')
        self.assertEqual(match.url_name, 'operator_list')

    def test_operator_list_template(self):
        url = reverse('operator_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/operator_list.html')
        self.assertEqual(response.status_code, 200)

    def test_operator_list_content(self):
        url = reverse('operator_list')
        response = self.client.get(url)
        for op in operator.objects.all():
            self.assertContains(response, op.name)

    def test_operator_activate(self):
        op = operator.objects.filter(is_active=False).first()
        url = reverse('operator_activate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = operator.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(op.is_active)

    def test_operator_deactivate(self):
        op = operator.objects.filter(is_active=True).first()
        url = reverse('operator_deactivate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = operator.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(op.is_active)


class TestProjectCRUD(TestCase):

    def setUp(self):
        mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        mommy.make(Project, name='project 2', slug='project-2', is_active=False)
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        mommy.make(operator, user=self.user, is_active=True)
        self.client.login(username='username1', password='')

    def test_project_list_resolution_template(self):
        url = '/projects/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'project_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/project_list.html')
        self.assertEqual(response.status_code, 200)

    def test_project_list_content(self):
        url = reverse('project_list')
        response = self.client.get(url)
        for project in Project.objects.all():
            self.assertContains(response, project.name)

    def test_project_detail_resolution_template(self):
        obj = Project.objects.filter(is_active=True).first()
        url = '/projects/{0}/'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'project_detail_all')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/project_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_content(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_detail_all', args=(obj.slug,))
        response = self.client.get(url)
        self.assertContains(response, obj.name)

    def test_project_detail_user_resolution_template(self):
        obj = Project.objects.filter(is_active=True).first()
        url = '/{0}/{1}/'.format(self.user.username, obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'project_detail_user')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/project_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_user_content(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_detail_user', args=(self.user.username,
                                                   obj.slug,))
        response = self.client.get(url)
        self.assertContains(response, obj.name)

    def test_project_create_resolution_template(self):
        url = '/projects/create/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'project_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/project_create.html')
        self.assertEqual(response.status_code, 200)

    def test_project_update_resolution_template(self):
        obj = Project.objects.filter(is_active=True).first()
        url = '/projects/{0}/edit/'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'project_update')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/project_update.html')
        self.assertEqual(response.status_code, 200)

    def test_project_activate(self):
        obj = Project.objects.filter(is_active=False).first()
        url = reverse('project_activate', args=(obj.slug,))
        list_url = reverse('project_list')
        response = self.client.get(url)
        obj = Project.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(obj.is_active)

    def test_project_deactivate(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_deactivate', args=(obj.slug,))
        list_url = reverse('project_list')
        response = self.client.get(url)
        obj = Project.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(obj.is_active)

    def test_project_track(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_track', args=(obj.slug,))
        list_url = reverse('project_list')
        response = self.client.get(url)
        self.assertRedirects(response, list_url)

        obj = Project.objects.get(id=obj.id)
        tracking = project_tracking.objects.get(project=obj)
        self.assertEqual(tracking.operator, self.user.operator)

    def test_project_untrack(self):
        obj = Project.objects.filter(is_active=True).first()
        tracking = project_tracking.objects.create(operator=self.user.operator,
                                                   project=obj)
        url = reverse('project_untrack', args=(obj.slug,))
        list_url = reverse('project_list')
        response = self.client.get(url)
        self.assertRedirects(response, list_url)

        obj = Project.objects.get(id=obj.id)
        tracking = project_tracking.objects.filter(project=obj).count()
        self.assertEqual(tracking, 0)

    def test_project_create_valid_data(self):
        url = reverse('project_create')
        data = {'name': 'project 3'}
        response = self.client.post(url, data)
        obj = Project.objects.get(**data)
        self.assertEqual(obj.slug, 'project-3')
        detail_url = reverse('project_detail_all', args=(obj.slug,))
        self.assertRedirects(response, detail_url)

    def test_project_create_empty_data(self):
        url = reverse('project_create')
        response = self.client.post(url, {})
        self.assertFormError(response, 'form', 'name',
            'This field is required.')

    def test_project_update_valid_data(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_update', args=(obj.slug,))
        data = {'description': 'test description'}
        response = self.client.post(url, data)
        obj = Project.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        detail_url = reverse('project_detail_all', args=(obj.slug,))
        self.assertRedirects(response, detail_url)


class TestInvestigationCRUD(TestCase):

    def setUp(self):
        project1 = mommy.make(Project, name='project 1', slug='project-1',
                              is_active=True)
        project2 = mommy.make(Project, name='project 2', slug='project-2',
                              is_active=False)

        mommy.make(Investigation, name='investigation 1',
                   slug='investigation-1', is_active=True, project=project1)
        mommy.make(Investigation, name='investigation 2',
                   slug='investigation-2', is_active=False, project=project2)

        user = get_user_model().objects.create_user('username1', password='')
        mommy.make(operator, user=user, is_active=True)
        self.client.login(username='username1', password='')

    def test_project_list_investigation_content(self):
        url = reverse('project_list')
        response = self.client.get(url)
        for investigation in Investigation.objects.all():
            if investigation.project.is_active:
                self.assertContains(response, investigation.name)
            else:
                self.assertNotContains(response, investigation.name)

    def test_investigation_detail_resolution_template(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = '/projects/{0}/{1}/'.format(proj.slug, obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'investigation_detail_all')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/investigation_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_detail_content(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = reverse('investigation_detail_all', args=(proj.slug, obj.slug))
        response = self.client.get(url)
        self.assertContains(response, obj.name)

    def test_investigation_create_resolution_template(self):
        proj = Project.objects.filter(is_active=True).first()
        url = '/projects/{0}/add-investigation/'.format(proj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'investigation_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/investigation_create.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_update_resolution_template(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = '/projects/{0}/{1}/edit/'.format(proj.slug, obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'investigation_update')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/investigation_update.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_activate(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = reverse('investigation_activate', args=(proj.slug, obj.slug))
        list_url = reverse('project_list')
        response = self.client.get(url)
        obj = Investigation.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(obj.is_active)

    def test_investigation_deactivate(self):
        obj = Investigation.objects.filter(is_active=True).first()
        proj = obj.project
        url = reverse('investigation_deactivate', args=(proj.slug, obj.slug))
        list_url = reverse('project_list')
        response = self.client.get(url)
        obj = Investigation.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(obj.is_active)

    def test_investigation_create_valid_data(self):
        proj = Project.objects.filter(is_active=True).first()
        url = reverse('investigation_create', args=(proj.slug,))
        data = {'name': 'investigation 3'}
        response = self.client.post(url, data)
        obj = Investigation.objects.get(**data)
        self.assertEqual(obj.slug, 'investigation-3')
        detail_url = reverse('investigation_detail_all',
                         args=(proj.slug, obj.slug,))
        self.assertRedirects(response, detail_url)

    def test_investigation_create_empty_data(self):
        proj = Project.objects.filter(is_active=True).first()
        url = reverse('investigation_create', args=(proj.slug,))
        response = self.client.post(url, {})
        self.assertFormError(response, 'form', 'name',
            'This field is required.')

    def test_investigation_update_valid_data(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = reverse('investigation_update', args=(proj.slug, obj.slug))
        data = {'description': 'test description'}
        response = self.client.post(url, data)
        obj = Investigation.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        detail_url = reverse('investigation_detail_all', args=(proj.slug, obj.slug,))
        self.assertRedirects(response, detail_url)
