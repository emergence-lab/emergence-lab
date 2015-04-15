# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d180readings',
            name='growth',
            field=models.ForeignKey(related_name='growth', to='d180.D180Growth'),
            preserve_default=True,
        ),
    ]
