# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0005_remove_d180growth_growth_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='d180growth',
            old_name='user',
            new_name='user_old',
        ),
    ]
