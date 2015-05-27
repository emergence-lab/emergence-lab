# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0011_rename_investigations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d180growth',
            name='investigations_old',
        ),
    ]
