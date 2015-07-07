# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20150630_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='investigation',
            field=models.ForeignKey(related_query_name='milestone', related_name='milestone', to='core.Investigation', null=True),
            preserve_default=True,
        ),
    ]
