# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141120_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='processnode',
            name='uid',
            field=models.SlugField(default='default', max_length=25, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
