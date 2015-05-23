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
        ('afm', '0002_afmfile_image_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AFMScan',
        ),
        migrations.RunPython(create_process_type),
    ]
