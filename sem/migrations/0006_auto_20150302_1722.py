# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0005_remove_semscan_image_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='semscan',
            name='image_number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semscan',
            name='image_source',
            field=models.CharField(default='esem_600', max_length=45, choices=[('leo1550', 'LEO 1550'), ('esem_600', 'FEI eSEM'), ('fib_1200', 'FEI Dual-Beam FIB')]),
            preserve_default=True,
        ),
    ]
