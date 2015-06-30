# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150618_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone_New',
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
                ('investigation', models.ForeignKey(related_query_name='milestone_new', related_name='milestone_new', to='core.Investigation', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'milestone',
                'verbose_name_plural': 'milestones',
            },
            bases=(models.Model,),
        ),
    ]
