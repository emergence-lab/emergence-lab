# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150521_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtype',
            name='full_name',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='processtype',
            name='name',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
