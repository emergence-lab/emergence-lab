# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0013_migrate_d180growth_data'),
        ('core', '0016_project_management'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SplitProcess',
        ),
    ]
