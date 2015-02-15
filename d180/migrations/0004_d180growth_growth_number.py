# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0003_auto_20150121_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='d180growth',
            name='growth_number',
            field=models.SlugField(default='g1000', max_length=10),
            preserve_default=False,
        ),
    ]
