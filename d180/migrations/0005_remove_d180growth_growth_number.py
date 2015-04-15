# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150406_0947'),
        ('d180', '0004_d180growth_growth_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d180growth',
            name='growth_number',
        ),
    ]
