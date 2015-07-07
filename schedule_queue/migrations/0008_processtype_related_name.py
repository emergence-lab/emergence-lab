# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0007_rename_tool_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='tool',
            field=models.ForeignKey(related_query_name='reservation', related_name='reservations', to='core.ProcessType'),
            preserve_default=True,
        ),
    ]
