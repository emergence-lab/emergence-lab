# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0002_progressupdate_milestone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('title', models.CharField(max_length=500)),
                ('external_id', models.CharField(max_length=100, blank=True)),
                ('abstract', core.models.fields.RichTextField(verbose_name='abstract', blank=True)),
                ('doi_number', models.CharField(max_length=100, blank=True)),
                ('year', models.CharField(max_length=4, blank=True)),
                ('journal', models.CharField(max_length=200, blank=True)),
                ('investigations', models.ManyToManyField(related_query_name='literature', related_name='literature', null=True, to='core.Investigation')),
                ('milestones', models.ManyToManyField(related_query_name='literature', related_name='literature', null=True, to='project_management.Milestone')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
