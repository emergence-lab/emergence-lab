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
        ('d180', '0013_migrate_d180growth_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='D180Growth',
        ),
        migrations.RunPython(create_process_type),
    ]
