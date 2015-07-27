# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_process_type(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')

    ProcessType.objects.create(type='afm',
                               is_destructive=False,
                               name='AFM',
                               full_name='Atomic Force Microscopy',
                               description='A very high-resolution scanning probe microscopy technique to characterize surface morphology.',
                               scheduling_type='none')


class Migration(migrations.Migration):

    dependencies = [
        ('afm', '0001_initial'),
        ('core', '0017_remove_splitprocess'),
    ]

    operations = [
        migrations.RunPython(create_process_type),
    ]
