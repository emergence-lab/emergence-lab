# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_process_types(apps, schema_editor):
    ProcessCategory = apps.get_model('core', 'ProcessCategory')
    ProcessType = apps.get_model('core', 'ProcessType')

    uncategorized, _ = ProcessCategory.objects.get_or_create(
        slug='uncategorized',
        name='Uncategorized',
        description='Uncategorized process types.')

    ProcessType.objects.get_or_create(
        type='generic-process',
        is_destructive=True,
        name='Generic',
        full_name='Generic Process',
        description='A generic process not covered by existing types.',
        scheduling_type='none',
        category=uncategorized)
    ProcessType.objects.get_or_create(
        type='split-process',
        is_destructive=False,
        name='Split',
        full_name='Split Sample',
        description='Splitting a sample into multiple pieces.',
        scheduling_type='none',
        category=uncategorized)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_process_types),
    ]
