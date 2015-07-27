# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0013_migrate_d180growth_data'),
        ('core', '0015_processtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('due_date', models.DateField()),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', editable=False)),
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
                ('investigation', models.ForeignKey(related_query_name='milestone', related_name='milestone', to='core.Investigation', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'milestone',
                'verbose_name_plural': 'milestones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MilestoneNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('note', core.models.fields.RichTextField(verbose_name='note', blank=True)),
                ('milestone', models.ForeignKey(related_query_name='note', related_name='note', to='core.Milestone', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('description', core.models.fields.RichTextField(verbose_name='description', blank=True)),
                ('due_date', models.DateField()),
                ('milestone', models.ForeignKey(related_query_name='task', related_name='task', to='core.Milestone', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='process',
            name='investigations',
            field=models.ManyToManyField(related_query_name='process', related_name='processes', to='core.Investigation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='milestones',
            field=models.ManyToManyField(related_query_name='milestone', related_name='processes', to='core.Milestone'),
            preserve_default=True,
        ),
    ]
