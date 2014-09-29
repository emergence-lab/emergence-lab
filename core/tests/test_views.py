# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils import timezone

from core.models import operator, platter


class TestHomepage(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('default', password='')

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

    def setUp(self):
        User = get_user_model()
        user1 = User.objects.create_user('username1', password='')
        user2 = User.objects.create_user('username2', password='')
        operator1 = operator.objects.create(name='name 1', user=user1,
                                            active=True)
        operator2 = operator.objects.create(name='name 2', user=user2,
                                            active=False)
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
        op = operator.objects.filter(active=False).first()
        url = reverse('operator_activate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = operator.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(op.active)

    def test_operator_deactivate(self):
        op = operator.objects.filter(active=True).first()
        url = reverse('operator_deactivate', args=(op.id,))
        list_url = reverse('operator_list')
        response = self.client.get(url)
        op = operator.objects.get(id=op.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(op.active)


class TestPlatterCRUD(TestCase):

    def setUp(self):
        platter.objects.bulk_create([
            platter(name='platter 1', active=True),
            platter(name='platter 2', active=False,
                    start_date=timezone.now() - timedelta(days=30),
                    end_date=timezone.now())
        ])
        get_user_model().objects.create_user('username1', password='')
        self.client.login(username='username1', password='')

    def test_platter_list_url_resolution(self):
        match = resolve('/platters/')
        self.assertEqual(match.url_name, 'platter_list')

    def test_platter_list_template(self):
        url = reverse('platter_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/platter_list.html')
        self.assertEqual(response.status_code, 200)

    def test_platter_list_content(self):
        url = reverse('platter_list')
        response = self.client.get(url)
        for plt in platter.objects.all():
            self.assertContains(response, plt.name)

    def test_platter_activate(self):
        obj = platter.objects.filter(active=False).first()
        url = reverse('platter_activate', args=(obj.id,))
        list_url = reverse('platter_list')
        response = self.client.get(url)
        obj = platter.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertTrue(obj.active)

    def test_platter_deactivate(self):
        obj = platter.objects.filter(active=True).first()
        url = reverse('platter_deactivate', args=(obj.id,))
        list_url = reverse('platter_list')
        response = self.client.get(url)
        obj = platter.objects.get(id=obj.id)

        self.assertRedirects(response, list_url)
        self.assertFalse(obj.active)
        self.assertEqual(timezone.now().date(), obj.end_date)
