# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150521_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtype',
            name='is_destructive',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processtype',
            name='name',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
