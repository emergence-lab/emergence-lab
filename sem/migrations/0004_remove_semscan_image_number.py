# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0003_auto_20150301_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semscan',
            name='image_number',
        ),
    ]
