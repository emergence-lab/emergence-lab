# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_add_field_user_milestone'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtype',
            name='scheduling_type',
            field=models.CharField(default='none', max_length=10, choices=[('none', 'None'), ('simple', 'Simple'), ('full', 'Full'), ('external', 'External')], blank=True, null=True),
            preserve_default=True,
        ),
    ]
