# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_processnode_piece'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='uid',
        ),
    ]
