# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_processtype(apps, schema_editor):
    ProcessType = apps.get_model('core', 'ProcessType')
    ProcessType.objects.create(type='d180-growth',
                               is_destructive=True,
                               name='D180',
                               full_name='D180 MOCVD Growth',
                               description='An MOCVD growth using the Veeco D180 reactor.',
                               scheduling_type='simple')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_splitprocess'),
        ('d180', '0013_migrate_d180growth_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d180growth',
            name='platter',
        ),
        migrations.RemoveField(
            model_name='d180growth',
            name='process_ptr',
        ),
        migrations.DeleteModel(
            name='D180Growth',
        ),
        migrations.RunPython(create_processtype),
    ]
