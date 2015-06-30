# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150630_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='milestones',
            field=models.ManyToManyField(related_query_name='milestone', related_name='processes', to='core.Milestone_New'),
            preserve_default=True,
        ),
    ]
