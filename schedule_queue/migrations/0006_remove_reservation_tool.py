# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0005_reservation_tool_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='tool',
        ),
    ]
