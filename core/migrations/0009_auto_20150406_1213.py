# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150406_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='content_type',
            field=models.CharField(default='', max_length=45, blank=True, choices=[('', 'Unknown'), ('application/octet-stream', 'Binary File'), ('image/png', 'PNG Image')]),
            preserve_default=True,
        ),
    ]
