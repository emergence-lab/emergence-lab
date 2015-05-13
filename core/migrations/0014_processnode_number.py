# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150426_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='processnode',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
