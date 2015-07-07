# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0003_rename_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='tool',
            field=models.CharField(max_length=100, choices=[(b'd180', b'D180'), (b'd75', b'D75')]),
            preserve_default=True,
        ),
    ]
