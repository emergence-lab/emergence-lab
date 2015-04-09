# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150409_0940'),
        ('d180', '0006_auto_20150409_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d180growth',
            name='user_old',
        ),
    ]
