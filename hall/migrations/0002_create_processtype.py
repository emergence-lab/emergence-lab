# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_process_type(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')
    ProcessType.objects.get_or_create(
        type='hall',
        is_destructive=False,
        name='Hall',
        full_name='Hall Effect Measurement',
        description='Measurement for carrier concentration and carrier mobility '
                    'based on the Hall effect.',
        scheduling_type='none')



class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0001_initial'),
        ('core', '0002_create_processtypes'),
    ]

    operations = [
        migrations.RunPython(create_process_type),
    ]
