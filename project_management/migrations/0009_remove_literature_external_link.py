# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0008_auto_20150628_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='literature',
            name='external_link',
        ),
    ]
