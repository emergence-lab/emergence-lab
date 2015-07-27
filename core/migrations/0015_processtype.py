# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import core.models.fields
from django.conf import settings


def create_default_process_types(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')

    ProcessType.objects.create(type='generic-process',
                               is_destructive=True,
                               name='Generic',
                               full_name='Generic Process',
                               description='A generic process not covered by existing types.',
                               scheduling_type='none')
    ProcessType.objects.create(type='split-process',
                               is_destructive=False,
                               name='Split',
                               full_name='Split Sample',
                               description='Splitting a sample into multiple pieces.',
                               scheduling_type='none')


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0013_migrate_d180growth_data'),
        ('core', '0014_processnode_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessType',
            fields=[
                ('type', models.SlugField(default='generic-process', max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=255)),
                ('is_destructive', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('scheduling_type', models.CharField(default='none', max_length=10, choices=[('none', 'None'), ('simple', 'Simple'), ('full', 'Full'), ('external', 'External')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_default_process_types),
        migrations.AddField(
            model_name='process',
            name='type',
            field=models.ForeignKey(default='generic-process', to='core.ProcessType'),
            preserve_default=True,
        ),
    ]
