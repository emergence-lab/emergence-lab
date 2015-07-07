# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0005_auto_20150602_1345'),
        ('core', '0017_remove_splitprocess'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='milestones',
            field=models.ManyToManyField(related_query_name='milestone', related_name='processes', to='project_management.Milestone'),
            preserve_default=True,
        ),
    ]
