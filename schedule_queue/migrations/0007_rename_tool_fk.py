# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0006_remove_reservation_tool'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='tool_fk',
            new_name='tool',
        ),
    ]
