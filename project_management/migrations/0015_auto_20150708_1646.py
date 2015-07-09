# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0014_auto_20150708_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='journal',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='literature',
            name='year',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
    ]
