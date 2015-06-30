# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20150630_1457'),
        ('project_management', '0012_remove_literature_milestones'),
    ]

    operations = [
        migrations.AddField(
            model_name='literature',
            name='milestones',
            field=models.ManyToManyField(related_query_name='literature', related_name='literature', null=True, to='core.Milestone'),
            preserve_default=True,
        ),
    ]
