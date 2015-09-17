# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from datetime import datetime

from model_mommy import mommy

from core.models import Project, ProjectTracking, Investigation, Milestone, MilestoneNote, Task


class TestDashboard(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_dashboard_resolution(self):
        url = '/dashboard/'
        name = 'dashboard'
        match = resolve(url)
        self.assertTemplateUsed(self.client.get(reverse(name)),
            'project_management/landing_page.html')
        self.assertEqual(match.url_name, name)


class TestNewsfeed(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.client.login(username='username1', password='')

    def test_newsfeed_resolution(self):
        url = '/dashboard/newsfeed'
        name = 'pm_newsfeed'
        match = resolve(url)
        self.assertTemplateUsed(self.client.get(reverse(name)),
            'project_management/newsfeed.html')
        self.assertEqual(match.url_name, name)


class TestProjectCRUD(TestCase):

    def setUp(self):
        mommy.make(Project, name='project 1', slug='project-1', is_active=True)
        mommy.make(Project, name='project 2', slug='project-2', is_active=False)
        project = Project.objects.first()
        mommy.make(Investigation, name='investigation 1',
            slug='investigation-1',
            project=project,
            is_active=True)
        self.user = get_user_model().objects.create_user('username1',
                                                         password='')
        self.user.groups.add(project.owner_group)
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
        self.assertContains(response, Investigation.objects.first().name)

    def test_project_update_valid_data(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('pm_project_edit', kwargs={'slug': obj.slug})
        data = {'name': obj.name, 'description': 'test description'}
        response = self.client.post(url, data)
        obj = Project.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        list_url = reverse('pm_project_detail', args=(obj.slug,))
        self.assertRedirects(response, list_url)

    def test_project_detail_content(self):
        obj = Project.objects.filter(is_active=True).first()
        url = reverse('pm_project_detail', kwargs={'slug': obj.slug})
        response = self.client.get(url)
        self.assertContains(response, obj.name)
        self.assertContains(response, Investigation.objects.first().name)

    def test_project_add_user(self):
        obj = Project.objects.filter(is_active=True).first()
        username = get_user_model().objects.create_user(username='username2',
                                                        password='')
        url = reverse('pm_project_group_add', kwargs={'slug': obj.slug,
                                                      'username': username.username,
                                                      'attribute': 'viewer'})
        response = self.client.get(url)
        self.assertEqual(obj.get_membership(username), 'viewer')
        self.assertRedirects(response, reverse('pm_project_detail', kwargs={'slug': obj.slug}))

    def test_project_remove_user(self):
        obj = Project.objects.filter(is_active=True).first()
        username = get_user_model().objects.create_user(username='username2',
                                                        password='')
        url = reverse('pm_project_group_remove', kwargs={'slug': obj.slug,
                                                         'username': username.username,})
        obj.add_user(username, 'viewer')
        self.assertEqual(obj.get_membership(username), 'viewer')
        response = self.client.get(url)
        self.assertIsNone(obj.get_membership(username))
        self.assertRedirects(response, reverse('pm_project_detail', kwargs={'slug': obj.slug}))


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
        ProjectTracking.objects.create(user=get_user_model().objects.first(), project=project1)

    def test_project_list_investigation_content(self):
        url = reverse('pm_project_list')
        response = self.client.get(url)
        for investigation in Investigation.objects.all():
            self.assertContains(response, investigation.name)

    def test_investigation_detail_resolution_template(self):
        obj = Investigation.objects.filter(is_active=True).first()
        url = '/dashboard/investigations/detail/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_investigation_detail')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/investigation_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_detail_content(self):
        obj = Investigation.objects.filter(is_active=False).first()
        url = reverse('pm_investigation_detail', kwargs={'slug': obj.slug})
        response = self.client.get(url)
        self.assertContains(response, obj.name)

    def test_investigation_create_resolution_template(self):
        proj = Project.objects.get(slug='project-1')
        url = '/dashboard/investigations/create/{}'.format(proj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_investigation_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/investigation_create.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_update_resolution_template(self):
        obj = Investigation.objects.filter(is_active=False).first()
        url = '/dashboard/investigations/edit/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'pm_investigation_edit')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/investigation_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_create_valid_data(self):
        proj = Project.objects.get(slug='project-1')
        url = reverse('pm_investigation_create', kwargs={'project': proj.slug})
        data = {'name': 'investigation 3', 'project': proj.id}
        response = self.client.post(url, data)
        obj = Investigation.objects.get(**data)
        self.assertEqual(obj.slug, 'investigation-3')
        detail_url = reverse('pm_investigation_detail',
                         args=(obj.slug,))
        self.assertRedirects(response, detail_url)

    def test_investigation_create_empty_data(self):
        proj = Project.objects.get(slug='project-1')
        url = reverse('pm_investigation_create', args=(proj.slug,))
        response = self.client.post(url, {})
        self.assertFormError(response, 'form', 'name',
            'This field is required.')

    def test_project_create_reserved_name(self):
        proj = Project.objects.get(slug='project-1')
        url = reverse('pm_investigation_create', args=(proj.slug,))
        data = {'name': 'activate'}
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'name',
            'Investigation name "activate" is reserved, please choose another')

    def test_investigation_update_valid_data(self):
        proj = Project.objects.get(slug='project-1')
        obj = Investigation.objects.filter(is_active=False).first()
        url = reverse('pm_investigation_edit', kwargs={'slug': obj.slug})
        data = {'name': obj.name, 'description': 'test description', 'project': proj.id}
        response = self.client.post(url, data)
        obj = Investigation.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        detail_url = reverse('pm_investigation_detail', kwargs={'slug': obj.slug})
        self.assertRedirects(response, detail_url)


class TestMilestoneCRUD(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('username1', password='')
        project1 = mommy.make(Project, name='project 1', slug='project-1',
                              is_active=True)
        project2 = mommy.make(Project, name='project 2', slug='project-2',
                              is_active=False)
        user.groups.add(project1.owner_group)
        user.groups.add(project2.owner_group)
        investigation1 = mommy.make(Investigation, name='investigation 1',
                   slug='investigation-1', is_active=True, project=project1)
        mommy.make(Milestone, name='milestone 1', slug='milestone-1',
            is_active=True, investigation=investigation1, user=get_user_model().objects.first())
        self.client.login(username='username1', password='')
        ProjectTracking.objects.create(user=get_user_model().objects.first(), project=project1)

    def test_milestone_list_content(self):
        url = reverse('milestone_list')
        response = self.client.get(url)
        for milestone in Milestone.objects.all():
            self.assertContains(response, milestone.name)

    def test_investigation_detail_resolution_template(self):
        obj = Milestone.objects.filter(is_active=True).first()
        url = '/dashboard/milestones/detail/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'milestone_detail')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/milestone_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_investigation_detail_content(self):
        obj = Milestone.objects.first()
        url = reverse('milestone_detail', kwargs={'slug': obj.slug})
        response = self.client.get(url)
        self.assertContains(response, obj.name)

    def test_milestone_create_resolution_template(self):
        investigation = Investigation.objects.get(slug='investigation-1')
        url = '/dashboard/milestones/create/{}'.format(investigation.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'milestone_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/milestone_create.html')
        self.assertEqual(response.status_code, 200)

    def test_milestone_update_resolution_template(self):
        obj = Milestone.objects.first()
        url = '/dashboard/milestones/edit/{0}'.format(obj.slug)
        match = resolve(url)
        self.assertEqual(match.url_name, 'milestone_edit')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/milestone_update.html')
        self.assertEqual(response.status_code, 200)

    def test_milestone_create_valid_data(self):
        investigation = Investigation.objects.get(slug='investigation-1')
        url = reverse('milestone_create', args=(investigation.slug,))
        due_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        data = {'name': 'Milestone 3', 'investigation': investigation.id,
            'user': get_user_model().objects.first().id, 'due_date': due_date}
        response = self.client.post(url, data)
        # print([(x.name, x.errors) for x in response.context['form']])
        obj = Milestone.objects.get(**data)
        self.assertEqual(obj.slug, 'milestone-3')
        detail_url = reverse('milestone_detail',
                         args=(obj.slug,))
        self.assertRedirects(response, detail_url)

    def test_milestone_create_empty_data(self):
        investigation = Investigation.objects.get(slug='investigation-1')
        url = reverse('milestone_create', args=(investigation.slug,))
        response = self.client.post(url, {})
        self.assertFormError(response, 'form', 'name',
            'This field is required.')

    def test_milestone_update_valid_data(self):
        investigation = Investigation.objects.get(slug='investigation-1')
        obj = Milestone.objects.first()
        url = reverse('milestone_edit', kwargs={'slug': obj.slug})
        due_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        data = {'name': obj.name, 'description': 'test description',
           'investigation': investigation.id, 'user': get_user_model().objects.first().id,
           'due_date': due_date}
        response = self.client.post(url, data)
        # print([(x.name, x.errors) for x in response.context['form']])
        obj = Milestone.objects.get(id=obj.id)
        self.assertEqual(obj.description, data['description'])
        detail_url = reverse('milestone_detail', kwargs={'slug': obj.slug})
        self.assertRedirects(response, detail_url)


class TestTaskCRUD(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('username1', password='')
        project1 = mommy.make(Project, name='project 1', slug='project-1',
                              is_active=True)
        user.groups.add(project1.owner_group)
        investigation1 = mommy.make(Investigation, name='investigation 1',
                   slug='investigation-1', is_active=True, project=project1)
        milestone1 = mommy.make(Milestone, name='milestone 1', slug='milestone-1',
            is_active=True, investigation=investigation1, user=get_user_model().objects.first())
        mommy.make(Task, description='task 1', is_active=True,
            milestone=milestone1, user=get_user_model().objects.first())
        self.client.login(username='username1', password='')
        ProjectTracking.objects.create(user=get_user_model().objects.first(), project=project1)

    def test_task_list_content(self):
        url = reverse('pm_task_list')
        response = self.client.get(url)
        for task in Task.objects.all():
            self.assertContains(response, task.description)

    def test_task_create_resolution_template(self):
        url = '/dashboard/tasks/new'
        match = resolve(url)
        self.assertEqual(match.url_name, 'task_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'project_management/task_create.html')
        self.assertEqual(response.status_code, 200)

    def test_task_create_action_valid_data(self):
        milestone = Milestone.objects.get(slug='milestone-1')
        url = reverse('milestone_task_action')
        due_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        data = {'description': 'description',
            # 'slug': milestone.slug,
            'milestone': milestone.id,
            'user': get_user_model().objects.first().id,
            'due_date': due_date}
        response = self.client.post(url, data)
        obj = Task.objects.get(description='description')
        self.assertEqual(obj.description, 'description')
        detail_url = reverse('milestone_detail', kwargs={'slug': milestone.slug})
        self.assertRedirects(response, detail_url)


class TestNoteCRUD(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('username1', password='')
        project1 = mommy.make(Project, name='project 1', slug='project-1',
                              is_active=True)
        user.groups.add(project1.owner_group)
        investigation1 = mommy.make(Investigation, name='investigation 1',
                   slug='investigation-1', is_active=True, project=project1)
        milestone1 = mommy.make(Milestone, name='milestone 1', slug='milestone-1',
            is_active=True, investigation=investigation1, user=get_user_model().objects.first())
        mommy.make(MilestoneNote, note='note-test', milestone=milestone1,
            user=get_user_model().objects.first())
        self.client.login(username='username1', password='')
        ProjectTracking.objects.create(user=get_user_model().objects.first(), project=project1)

    def test_note_list_content(self):
        note = MilestoneNote.objects.first()
        url = reverse('milestone_detail', kwargs={'slug': note.milestone.slug})
        response = self.client.get(url)
        for task in Task.objects.all():
            self.assertContains(response, task.description)

    def test_note_create_action_valid_data(self):
        milestone = Milestone.objects.get(slug='milestone-1')
        url = reverse('milestone_note_action')
        data = {'note': 'note',
            # 'slug': milestone.slug,
            'milestone': milestone.id,
            'user': get_user_model().objects.first().id}
        response = self.client.post(url, data)
        obj = MilestoneNote.objects.get(note='note')
        self.assertEqual(obj.note, 'note')
        detail_url = reverse('milestone_detail', kwargs={'slug': obj.milestone.slug})
        self.assertRedirects(response, detail_url)
