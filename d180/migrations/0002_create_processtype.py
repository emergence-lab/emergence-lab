# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_process_type(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')
    ProcessType.objects.get_or_create(
        type='d180-growth',
        is_destructive=True,
        name='D180',
        full_name='D180 MOCVD Growth',
        description='An MOCVD growth using the Veeco D180 reactor.',
        scheduling_type='simple')


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_process_type),
    ]
