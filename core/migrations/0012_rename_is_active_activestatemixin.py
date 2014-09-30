# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investigation',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='operator',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='platter',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='active',
            new_name='is_active',
        ),
    ]
