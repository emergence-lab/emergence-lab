# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0009_remove_literature_external_link'),
        ('core', '0019_auto_20150630_1426')
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='milestones',
            field=models.ManyToManyField(related_query_name='literature', related_name='literature', null=True, to='core.Milestone_New'),
            preserve_default=True,
        ),
    ]
