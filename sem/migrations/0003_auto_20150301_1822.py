# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0002_auto_20150228_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semscan',
            name='file',
        ),
        migrations.AddField(
            model_name='semscan',
            name='image',
            field=models.ImageField(max_length=150, null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='semscan',
            name='image_source',
            field=models.CharField(default='esem_600', max_length=45, choices=[('leo1550', 'LEO 1550'), ('esem_600', 'FEI eSEM'), ('fib_1200', 'FEI Dual-Beam FIB')]),
            preserve_default=True,
        ),
    ]
