# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveStateModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(editable=False, null=True, verbose_name='status changed', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AutoUUIDModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParentProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='core.Process')),
                ('parent_field', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
        migrations.CreateModel(
            name='ChildProcess',
            fields=[
                ('parentprocess_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='tests.ParentProcess')),
                ('child_field', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.parentprocess',),
        ),
        migrations.CreateModel(
            name='UUIDModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('uuid_full', core.models.fields.UUIDField(max_length=32, blank=True, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
