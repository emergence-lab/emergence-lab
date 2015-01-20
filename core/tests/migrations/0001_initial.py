# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentProcess',
            fields=[
                ('process_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='core.Process')),
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
                ('parentprocess_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='tests.ParentProcess')),
                ('child_field', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.parentprocess',),
        ),
    ]
