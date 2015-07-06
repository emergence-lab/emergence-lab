# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0002_add_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='bake_length_in_minutes',
            new_name='bake_length',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='growth_length_in_hours',
            new_name='growth_length',
        ),
    ]
