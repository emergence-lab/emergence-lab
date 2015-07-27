# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0010_fk_to_process'),
    ]

    operations = [
        migrations.RenameField(
            model_name='d180growth',
            old_name='investigations',
            new_name='investigations_old',
        ),
    ]
