# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_sample_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='uid',
            field=models.SlugField(max_length=25, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
