# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0004_remove_semscan_image_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semscan',
            name='image_source',
        ),
    ]
