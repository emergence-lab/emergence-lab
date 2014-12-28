# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='priority_field',
            field=models.BigIntegerField(default=9223372036854775807),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='tool',
            field=models.CharField(max_length=10, choices=[(b'd180', b'D180'), (b'd75', b'D75')]),
            preserve_default=True,
        ),
    ]
