# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0003_move_platter'),
        ('core', '0013_status_changed_not_editable'),
    ]

    operations = [
        migrations.DeleteModel(
            name='platter',
        ),
    ]
