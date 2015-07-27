# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_splitprocess'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='polymorphic_ctype',
        ),
    ]
