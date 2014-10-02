# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_is_active_activestatemixin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='status_changed',
            field=models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='status_changed',
            field=models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='platter',
            name='status_changed',
            field=models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status_changed',
            field=models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True),
        ),
    ]
