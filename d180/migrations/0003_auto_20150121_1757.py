# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0002_auto_20150121_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d180readings',
            name='growth',
            field=models.ForeignKey(related_name='readings', to='d180.D180Growth'),
            preserve_default=True,
        ),
    ]
