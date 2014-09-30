# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_change_investigation'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigation',
            name='status_changed',
            field=models.DateTimeField(null=True, verbose_name='status changed', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operator',
            name='status_changed',
            field=models.DateTimeField(null=True, verbose_name='status changed', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='platter',
            name='status_changed',
            field=models.DateTimeField(null=True, verbose_name='status changed', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='status_changed',
            field=models.DateTimeField(null=True, verbose_name='status changed', blank=True),
            preserve_default=True,
        ),
    ]
