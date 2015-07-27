# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0008_d180growthinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='d180readings',
            old_name='growth',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='d180readings',
            old_name='layer_desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='d180recipelayer',
            old_name='growth',
            new_name='process',
        ),
    ]
