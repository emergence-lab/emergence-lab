# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141120_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='uid',
            field=models.SlugField(max_length=25, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
