# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='command',
            field=models.CharField(default=b'sdevice', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='runfile',
            field=models.CharField(default='des.cmd', max_length=12, blank=True),
            preserve_default=False,
        ),
    ]
