# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_process_investigations'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SplitProcess',
        ),
    ]
