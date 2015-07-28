# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_process_type(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')
    ProcessType.objects.get_or_create(
        type='sem',
        is_destructive=False,
        name='SEM',
        full_name='Scanning Electron Microscopy',
        description='A microscopy technique that uses focused beams of '
                    'electrons to image a sample.',
        scheduling_type='none')


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_process_type),
    ]
