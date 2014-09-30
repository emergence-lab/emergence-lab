# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_migrate_platter_end_date_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platter',
            name='end_date',
        ),
    ]
