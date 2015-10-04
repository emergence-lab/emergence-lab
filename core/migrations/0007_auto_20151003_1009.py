# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_project_management_fks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='user',
        ),
        migrations.RemoveField(
            model_name='milestonenote',
            name='user',
        ),
    ]
