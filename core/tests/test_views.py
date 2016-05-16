# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test import TestCase
from django.forms import ValidationError

from model_mommy import mommy

from .helpers import test_resolution_template
from core.models import (Investigation, Process, Project, ProjectTracking,
                         Sample, Substrate, ProcessTemplate, ProcessType,
                         ProcessCategory)


class TestHomepageAbout(TestCase):

    def test_homepage_url_resolution(self):
        match = resolve('/')
        self.assertEqual(match.url_name, 'home')

    def test_homepage_access_anonymous(self):
        self.client.logout()

        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)

    def test_homepage_access_login(self):
        get_user_model().objects.create_user('default', password='')
        result = self.client.login(username='default', password='')
        self.assertTrue(result)

        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)

    def test_about_url_resolution(self):
        url = '/about/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'about')

    def test_about_access_anonymous(self):
        self.client.logout()

        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertEqual(response.status_code, 200)

    def test_about_access_login(self):
        get_user_model().objects.create_user('default', password='')
        result = self.client.login(username='default', password='')
        self.assertTrue(result)

        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertEqual(response.status_code, 200)


class TestUserCRUD(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
        user = get_user_model().objects.create_user('username2', password='')
        user.is_active = False
        user.save()
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
        User = get_user_model()
        url = reverse('operator_list')
        response = self.client.get(url)
        for op in User.objects.all():
            self.assertContains(response, op.short_name)

    def test_operator_activate(self):
        User = get_user_model()
        op = User.objects.filter(is_active=False).first()
        url = reverse('operator_activate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = User.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(op.is_active)

    def test_operator_deactivate(self):
        User = get_user_model()
        op = User.objects.filter(is_active=True).first()
        url = reverse('operator_deactivate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = User.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(op.is_active)


class TestProjectCRUD(TestCase):

    def setUp(self):
        proj1 = mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        proj2 = mommy.make(Project, name='project 2', slug='project-2', is_active=False)
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        proj1.add_user(self.user, 'owner')
        proj2.add_user(self.user, 'owner')
        self.client.login(username='username1', password='')

    def test_project_list_resolution_template(self):
        url = '/dashboard/projects/'
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_project_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/project_list.html')
        self.assertEqual(response.status_code, 200)

    def test_project_list_content(self):
        url = reverse('pm_project_list')
        response = self.client.get(url)
        for project in Project.objects.all():
            self.assertContains(response, project.name)

    def test_project_detail_resolution_template(self):
        obj = Project.objects.filter(is_active=True).first()
        url = '/dashboard/projects/detail/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_project_detail')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/project_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_content(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('pm_project_detail', args=(obj.slug,))
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
        url = '/dashboard/projects/edit/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_project_edit')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/project_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_project_activate(self):
        obj = Project.objects.filter(is_active=False).first()
        url = reverse('project_activate', args=(obj.slug,))
        redirect_url = reverse('pm_project_detail', args=(obj.slug,))
        response = self.client.get(url)
        obj = Project.objects.get(id=obj.id)

        self.assertRedirects(response, redirect_url)
        self.assertTrue(obj.is_active)

    def test_project_deactivate(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_deactivate', args=(obj.slug,))
        redirect_url = reverse('pm_project_detail', args=(obj.slug,))
        response = self.client.get(url)
        obj = Project.objects.get(id=obj.id)

        self.assertRedirects(response, redirect_url)
        self.assertFalse(obj.is_active)

    def test_project_track(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('project_track', args=(obj.slug,))
        list_url = reverse('pm_project_list')
        response = self.client.get(url)
        self.assertRedirects(response, list_url)

        obj = Project.objects.get(id=obj.id)
        tracking = ProjectTracking.objects.get(project=obj)
        self.assertEqual(tracking.user, self.user)

    def test_project_untrack(self):
        obj = Project.objects.filter(is_active=True).first()
        tracking = ProjectTracking.objects.create(user=self.user, project=obj)
        url = reverse('project_untrack', args=(obj.slug,))
        list_url = reverse('pm_project_list')
        response = self.client.get(url)
        self.assertRedirects(response, list_url)

        obj = Project.objects.get(id=obj.id)
        tracking = ProjectTracking.objects.filter(project=obj).count()
        self.assertEqual(tracking, 0)

    def test_project_create_valid_data(self):
        url = reverse('project_create')
        data = {'name': 'project 3'}
        response = self.client.post(url, data)
        obj = Project.objects.get(**data)
        self.assertEqual(obj.slug, 'project-3')
        detail_url = reverse('pm_project_list')
        self.assertRedirects(response, detail_url)

    def test_project_create_empty_data(self):
        url = reverse('project_create')
        response = self.client.post(url, {})
        self.assertFormError(response, 'form', 'name',
            'This field is required.')

    def test_project_create_reserved_name(self):
        url = reverse('project_create')
        data = {'name': 'create'}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'name',
            'Project name "create" is reserved, please choose another')

    def test_project_update_valid_data(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('pm_project_edit', args=(obj.slug,))
        data = {'name': obj.name, 'description': 'test description'}
        response = self.client.post(url, data)
        obj = Project.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        detail_url = reverse('pm_project_detail', args=(obj.slug,))
        self.assertRedirects(response, detail_url)


class TestInvestigationCRUD(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('username1', password='')
        project1 = mommy.make(Project, name='project 1', slug='project-1',
                              is_active=True)
        project2 = mommy.make(Project, name='project 2', slug='project-2',
                              is_active=False)
        user.groups.add(project1.owner_group)
        user.groups.add(project2.owner_group)

        mommy.make(Investigation, name='investigation 1',
                   slug='investigation-1', is_active=True, project=project1)
        mommy.make(Investigation, name='investigation 2',
                   slug='investigation-2', is_active=False, project=project2)
        self.client.login(username='username1', password='')

    def test_project_list_investigation_content(self):
        url = reverse('pm_project_list')
        response = self.client.get(url)
        for investigation in Investigation.objects.all():
            self.assertContains(response, investigation.name)

    def test_investigation_activate(self):
        obj = Investigation.objects.filter(is_active=False).first()
        proj = obj.project
        url = reverse('investigation_activate', args=(proj.slug, obj.slug))
        redirect_url = reverse('pm_investigation_detail', args=(obj.slug,))
        response = self.client.get(url)
        obj = Investigation.objects.get(id=obj.id)

        self.assertRedirects(response, redirect_url)
        self.assertTrue(obj.is_active)

    def test_investigation_deactivate(self):
        obj = Investigation.objects.filter(is_active=True).first()
        proj = obj.project
        url = reverse('investigation_deactivate', args=(proj.slug, obj.slug))
        redirect_url = reverse('pm_investigation_detail', args=(obj.slug,))
        response = self.client.get(url)
        obj = Investigation.objects.get(id=obj.id)

        self.assertRedirects(response, redirect_url)
        self.assertFalse(obj.is_active)


class TestSampleCRUD(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('username1', password='')
        self.client.login(username='username1', password='')

    def test_sample_list_resolution_template(self):
        test_resolution_template(self,
            url='/samples/',
            url_name='sample_list',
            template_file='core/sample_list.html',
            response_code=200)

    def test_sample_list_content(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        url = reverse('sample_list')
        response = self.client.get(url)
        self.assertContains(response, sample.uuid)

    def test_sample_detail_resolution_template(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        test_resolution_template(self,
            url='/samples/{}/'.format(sample.uuid),
            url_name='sample_detail',
            template_file='core/sample_detail.html',
            response_code=200,
            valid_lookup=sample.uuid,
            invalid_lookup='s1000')

    def test_sample_detail_content(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        url = reverse('sample_detail', args=(sample.uuid,))
        response = self.client.get(url)
        self.assertContains(response, sample.uuid)

    def test_sample_create_resolution_template(self):
        test_resolution_template(self,
            url='/samples/create/',
            url_name='sample_create',
            template_file='core/sample_create.html',
            response_code=200)

    def test_sample_create_empty_data(self):
        url = reverse('sample_create')
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', '',
                             'Cannot leave all substrate fields blank.')

    def test_sample_create_valid_data(self):
        url = reverse('sample_create')
        data = {
            'sample-comment': 'test sample',
            'substrate-comment': 'test sub',
            'substrate-serial': 'serial',
            'substrate-source': 'source',
        }
        response = self.client.post(url, data)
        sample = Sample.objects.last()
        detail_url = reverse('sample_detail', args=(sample.uuid,))
        self.assertRedirects(response, detail_url)
        self.assertEqual(sample.comment, data['sample-comment'])
        self.assertEqual(sample.substrate.comment, data['substrate-comment'])

    def test_sample_edit_resolution_template(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        test_resolution_template(self,
            url='/samples/{}/edit/'.format(sample.uuid),
            url_name='sample_edit',
            template_file='core/sample_edit.html',
            response_code=200,
            valid_lookup=sample.uuid,
            invalid_lookup='s1000')

    def test_sample_edit_valid_data(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        url = reverse('sample_edit', args=(sample.uuid,))
        data = {'comment': 'testing'}
        response = self.client.post(url, data)
        sample = Sample.objects.get_by_uuid(sample.uuid)
        self.assertEqual(sample.comment, data['comment'])
        detail_url = reverse('sample_detail', args=(sample.uuid,))
        self.assertRedirects(response, detail_url)


class TestProcessCRUD(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_process_list_resolution_template(self):
        test_resolution_template(self,
            url='/process/list/all/all/',
            url_name='process_list',
            template_file='core/process_list.html',
            response_code=200)

    def test_process_list_content(self):
        process = mommy.make(Process)
        url = reverse('process_list', kwargs={'slug': 'all', 'username': 'all'})
        response = self.client.get(url)
        self.assertContains(response, process.uuid)

    def test_process_detail_resolution_template(self):
        process = mommy.make(Process)
        test_resolution_template(self,
            url='/process/{}/'.format(process.uuid),
            url_name='process_detail',
            template_file='core/process_detail.html',
            response_code=200,
            valid_lookup=process.uuid,
            invalid_lookup='p0000000')

    def test_process_detail_content(self):
        process = mommy.make(Process)
        sample = Sample.objects.create(mommy.make(Substrate))
        sample.run_process(process)
        url = reverse('process_detail', args=(process.uuid,))
        response = self.client.get(url)
        self.assertContains(response, process.uuid)
        self.assertContains(response, sample.uuid)

    def test_process_edit_resolution_template(self):
        process = mommy.make(Process)
        test_resolution_template(self,
            url='/process/{}/edit/'.format(process.uuid),
            url_name='process_edit',
            template_file='core/process_edit.html',
            response_code=200,
            valid_lookup=process.uuid,
            invalid_lookup='p0000000')

    def test_process_edit_empty_data(self):
        process = mommy.make(Process)
        url = '/process/{}/edit/'.format(process.uuid)
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_process_edit_valid_data(self):
        process = mommy.make(Process)
        url = '/process/{}/edit/'.format(process.uuid)
        data = {
            'title': process.title,
            'comment': 'testing',
        }
        response = self.client.post(url, data)
        process = Process.objects.get(id=process.id)
        self.assertEqual(process.comment, data['comment'])
        detail_url =  '/process/{}/'.format(process.uuid)
        self.assertRedirects(response, detail_url)

    def test_process_wizard_resolution_template(self):
        test_resolution_template(self,
            url='/process/create/',
            url_name='process_create',
            template_file='core/process_wizard_create.html',
            response_code=200)

    def test_process_wizard_empty_data(self):
        url = '/process/create/'
        with self.assertRaises(ValidationError) as cm:
            self.client.post(url, {})
        exception = cm.exception
        self.assertEqual(exception.message,
            'ManagementForm data is missing or has been tampered with')

    def test_process_wizard_valid_data(self):
        url = '/process/create/'
        sample = Sample.objects.create(mommy.make(Substrate))
        processtype = mommy.make(ProcessType, type='test')
        data = {
            'process-title': 'title',
            'process-comment': 'testing',
            'process-user': self.user.id,
            'process-type': processtype.type,
            'sample-0-existing_or_new': 'existing-sample',
            'sample-0-sample_uuid': '{}'.format(sample.uuid),
            'sample-INITIAL_FORMS': '1',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '1'
        }
        response = self.client.post(url, data)
        process = Process.objects.last()
        self.assertEqual(process.comment, data['process-comment'])
        detail_url =  '/process/{}/'.format(process.uuid)
        self.assertRedirects(response, detail_url)

    def test_process_wizard_valid_multiple(self):
        url = reverse('process_create')
        samples = [
            Sample.objects.create(substrate=mommy.make(Substrate)),
            Sample.objects.create(substrate=mommy.make(Substrate)),
        ]
        processtype = mommy.make(ProcessType, type='test')
        data = {
            'process-title': 'title',
            'process-comment': 'testing',
            'process-user': self.user.id,
            'process-type': processtype.type,
            'sample-0-existing_or_new': 'existing-sample',
            'sample-0-sample_uuid': samples[0].uuid,
            'sample-1-existing_or_new': 'existing-sample',
            'sample-1-sample_uuid': samples[1].uuid,
            'sample-INITIAL_FORMS': '2',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '2',
        }
        response = self.client.post(url, data)
        process = Process.objects.last()
        self.assertEqual(process.comment, data['process-comment'])
        nodes = process.processnode_set.all()
        for n, (node, sample) in enumerate(zip(nodes, samples)):
            self.assertEqual(node.number, n + 1)
            self.assertEqual(node.get_sample().uuid, sample.uuid)
        detail_url = reverse('process_detail', args=(process.uuid,))
        self.assertRedirects(response, detail_url)

    def test_process_wizard_ambiguous_piece(self):
        url = '/process/create/'
        sample = Sample.objects.create(mommy.make(Substrate))
        sample.split(self.user, 2)
        processtype = mommy.make(ProcessType, type='test')
        data = {
            'process-title': 'title',
            'process-comment': 'testing',
            'process-user': self.user.id,
            'process-type': processtype.type,
            'sample-0-existing_or_new': 'existing-sample',
            'sample-0-sample_uuid': '{}'.format(sample.uuid),
            'sample-INITIAL_FORMS': '1',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '1'
        }
        response = self.client.post(url, data)
        self.assertFormsetError(response, 'sample_formset', 0, 'sample_uuid',
            'Sample {} is ambiguous, piece needs to be specified'.format(sample.uuid))

    def test_process_wizard_sample_piece(self):
        url = '/process/create/'
        sample = Sample.objects.create(mommy.make(Substrate))
        sample.split(self.user, 2)
        piece = 'b'
        processtype = mommy.make(ProcessType, type='test')
        data = {
            'process-title': 'title',
            'process-comment': 'testing',
            'process-user': self.user.id,
            'process-type': processtype.type,
            'sample-0-existing_or_new': 'existing-sample',
            'sample-0-sample_uuid': '{}{}'.format(sample.uuid, piece),
            'sample-INITIAL_FORMS': '1',
            'sample-MAX_NUM_FORMS': '',
            'sample-TOTAL_FORMS': '1'
        }
        response = self.client.post(url, data)
        nodes = sample.get_nodes_for_process_type(processtype.type)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].piece, piece)

    def test_process_autocreate_resolution_template(self):
        sample = Sample.objects.create(mommy.make(Substrate))
        test_resolution_template(self,
            url='/process/autocreate/{}/'.format(sample.uuid),
            url_name='process_autocreate',
            template_file='core/process_create.html',
            response_code=200,
            valid_lookup=sample.uuid,
            invalid_lookup='s1000')

    def test_autocreate_empty_data(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('process_autocreate', args=[sample.uuid])
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'pieces', 'This field is required.')

    def test_process_autocreate_invalid_pieces(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('process_autocreate', args=[sample.uuid])
        data = {
            'title': 'process title',
            'pieces': ['b'],
            'type': 'generic-process',
        }
        response = self.client.post(url, data)

        msg = 'Select a valid choice. b is not one of the available choices.'
        self.assertFormError(response, 'form', 'pieces', msg)

    def test_process_autocreate_invalid_title(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('process_autocreate', args=[sample.uuid])
        data = {
            'title': '',
            'pieces': ['a'],
            'type': 'generic-process',
        }
        response = self.client.post(url, data)

        msg = 'This field is required.'
        self.assertFormError(response, 'form', 'title', msg)

    def test_process_autocreate_invalid_type(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('process_autocreate', args=[sample.uuid])
        data = {
            'title': 'process title',
            'pieces': ['a'],
            'type': 'nonexistant',
        }
        response = self.client.post(url, data)

        msg = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertFormError(response, 'form', 'type', msg)

    def test_process_autocreate_valid_data(self):
        sample = Sample.objects.create(substrate=mommy.make(Substrate))
        url = reverse('process_autocreate', args=[sample.uuid])
        data = {
            'title': 'process title',
            'pieces': ['a'],
            'type': 'generic-process',
        }
        response = self.client.post(url, data)
        process = Process.objects.last()
        self.assertRedirects(response, reverse('process_detail', args=[process.uuid]))


class TestProcessTemplateCRUD(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_create_process_template(self):
        process = mommy.make(Process)
        url = '/process/templates/add/{}/'.format(process.uuid)
        response = self.client.get(url)
        template = ProcessTemplate.objects.last()
        self.assertEqual(template.id, 1)
        detail_url = '/process/templates/detail/{}/'.format(template.id)
        self.assertRedirects(response, detail_url)

    def test_edit_process_template(self):
        process = mommy.make(Process)
        template = ProcessTemplate.objects.create(process=process,
                                                  user=self.user)
        url = '/process/templates/{}/edit/'.format(template.id)
        data = {
            'name': 'test',
            'title': 'process title',
            'comment': 'test_comment'
        }
        response = self.client.post(url, data)
        detail_url = '/process/templates/detail/{}/'.format(template.id)
        self.assertRedirects(response, detail_url)
        comment = ProcessTemplate.objects.get(id=template.id).comment
        self.assertEqual(comment, data['comment'])

    def test_delete_process_template(self):
        process = mommy.make(Process)
        template = ProcessTemplate.objects.create(process=process,
                                                  user=self.user)
        url = '/process/templates/{}/remove/'.format(template.id)
        response = self.client.post(url, args=(template.id,), follow=True)
        with self.assertRaises(ProcessTemplate.DoesNotExist):
            ProcessTemplate.objects.get(id=template.id)
        self.assertEqual(response.status_code, 200)


class TestProcessTypeCRUD(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_processtype_list_resolution_template(self):
        test_resolution_template(self,
            url='/process/type/',
            url_name='processtype_list',
            template_file='core/processtype_list.html',
            response_code=200)

    def test_processtype_list_content(self):
        processtype = mommy.make(ProcessType, type='test')
        url = reverse('processtype_list')
        response = self.client.get(url)
        self.assertContains(response, processtype.full_name)

    def test_processtype_detail_resolution_template(self):
        processtype = mommy.make(ProcessType, type='test')
        test_resolution_template(self,
            url='/process/type/{}/'.format(processtype.type),
            url_name='processtype_detail',
            template_file='core/processtype_detail.html',
            response_code=200,
            valid_lookup='test',
            invalid_lookup='invalid')

    def test_processtype_detail_content(self):
        processtype = mommy.make(ProcessType, type='test')
        url = reverse('processtype_detail', args=(processtype.type,))
        response = self.client.get(url)
        self.assertContains(response, processtype.full_name)

    def test_processtype_edit_resolution_template(self):
        processtype = mommy.make(ProcessType, type='test')
        test_resolution_template(self,
            url='/process/type/{}/edit/'.format(processtype.type),
            url_name='processtype_edit',
            template_file='core/processtype_edit.html',
            response_code=200,
            valid_lookup='test',
            invalid_lookup='invalid')

    def test_processtype_edit_empty_data(self):
        processtype = mommy.make(ProcessType, type='test')
        url = reverse('processtype_edit', args=(processtype.type,))
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_processtype_edit_valid_data(self):
        processcategory = mommy.make(ProcessCategory)
        processtype = mommy.make(ProcessType, type='test', category=processcategory)
        url = reverse('processtype_edit', args=(processtype.type,))
        data = {
            'name': processtype.name,
            'full_name': processtype.full_name,
            'description': 'testing',
            'is_destructive': processtype.is_destructive,
            'category': processtype.category_id,
            'scheduling_type': processtype.scheduling_type,
            'creation_type': processtype.creation_type,
        }
        response = self.client.post(url, data)
        processtype = ProcessType.objects.get(type=processtype.type)
        self.assertEqual(processtype.description, data['description'])
        detail_url =  '/process/type/{}/'.format(processtype.type)
        self.assertRedirects(response, detail_url)

    def test_processtype_create_resolution_template(self):
        test_resolution_template(self,
            url='/process/type/create/',
            url_name='processtype_create',
            template_file='core/processtype_create.html',
            response_code=200)

    def test_processtype_create_empty_data(self):
        url = reverse('processtype_create')
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'type',
                             'This field is required.')

    def test_processtype_create_valid_data(self):
        processcategory = mommy.make(ProcessCategory)
        url = reverse('processtype_create')
        data = {
            'type': 'test',
            'name': 'Test',
            'full_name': 'Test Process',
            'description': 'testing',
            'is_destructive': True,
            'category': processcategory.slug,
            'scheduling_type': 'none',
            'creation_type': 'default',
        }
        response = self.client.post(url, data)
        processtype = ProcessType.objects.last()
        self.assertRedirects(response, reverse('processtype_detail',
                                               args=(processtype.type,)))

    def test_processcategory_create_resolution_template(self):
        test_resolution_template(self,
            url='/process/type/category/create/',
            url_name='processcategory_create',
            template_file='core/processtype_create.html',
            response_code=200)

    def test_processcategory_create_empty_data(self):
        url = reverse('processcategory_create')
        data = {}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'slug',
                             'This field is required.')

    def test_processcategory_create_valid_data(self):
        url = reverse('processcategory_create')
        data = {
            'slug': 'test',
            'name': 'Test',
            'description': 'testing',
        }
        response = self.client.post(url, data)
        processcategory = ProcessCategory.objects.last()
        self.assertRedirects(response, reverse('processtype_list'))
