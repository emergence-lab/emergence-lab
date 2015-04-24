# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150422_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtemplate',
            name='name',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
