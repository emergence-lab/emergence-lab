# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.db import models, migrations


def create_process_type(apps, schema_editor):
    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, 'process_type.json'), 'r') as f:
        data = json.load(f)

    ProcessType = apps.get_model('core', 'ProcessType')
    ProcessType.objects.create(**data)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_processtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='HallData',
            fields=[
                ('datafile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.DataFile')),
                ('temperature', models.DecimalField(default=300.0, max_digits=7, decimal_places=2, blank=True)),
                ('symmetry_factor', models.DecimalField(default=1.0, max_digits=7, decimal_places=2, blank=True)),
                ('sheet_coefficient', models.FloatField(null=True, blank=True)),
                ('sheet_resistance', models.FloatField(null=True, blank=True)),
                ('sheet_concentration', models.FloatField(null=True, blank=True)),
                ('thickness', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('mobility', models.FloatField(null=True, blank=True)),
                ('bulk_coefficient', models.FloatField(null=True, blank=True)),
                ('bulk_resistance', models.FloatField(null=True, blank=True)),
                ('bulk_concentration', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.datafile',),
        ),
        migrations.RunPython(create_process_type),
    ]
