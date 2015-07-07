# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150630_1441'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Milestone_New',
            new_name='Milestone',
        ),
    ]
