# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_sample_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='uid',
            field=models.SlugField(default='default', max_length=25, blank=True),
            preserve_default=False,
        ),
    ]
