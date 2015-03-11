# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sem.models


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0006_auto_20150302_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semscan',
            name='image',
            field=models.ImageField(max_length=150, null=True, upload_to=sem.models.get_file_path, blank=True),
            preserve_default=True,
        ),
    ]
