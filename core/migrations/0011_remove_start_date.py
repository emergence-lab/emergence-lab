# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_add_timestampmixin_migrate_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investigation',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='start_date',
        ),
    ]
