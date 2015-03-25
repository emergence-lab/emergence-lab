# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150324_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='content_type',
            field=models.CharField(max_length=45, null=True, blank=True),
            preserve_default=True,
        ),
    ]
