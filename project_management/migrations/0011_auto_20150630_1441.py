# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150630_1441'),
        ('project_management', '0010_auto_20150630_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='investigation',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='user',
        ),
        migrations.DeleteModel(
            name='Milestone',
        ),
    ]
