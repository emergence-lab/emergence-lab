# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 19:31
from __future__ import unicode_literals

import core.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('title', models.CharField(max_length=500)),
                ('external_id', models.CharField(blank=True, max_length=100)),
                ('abstract', core.models.fields.RichTextField(blank=True, null=True, verbose_name='abstract')),
                ('doi_number', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('journal', models.CharField(blank=True, max_length=200, null=True)),
                ('investigations', models.ManyToManyField(related_name='literature', related_query_name='literature', to='core.Investigation')),
                ('milestones', models.ManyToManyField(related_name='literature', related_query_name='literature', to='core.Milestone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
