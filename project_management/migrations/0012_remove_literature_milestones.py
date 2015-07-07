# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0011_auto_20150630_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='literature',
            name='milestones',
        ),
    ]
