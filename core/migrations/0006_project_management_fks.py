# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150813_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(related_query_name='investigation', related_name='investigations', verbose_name='project', to='core.Project'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='investigation',
            field=models.ForeignKey(related_query_name='milestone', related_name='milestones', to='core.Investigation', null=True),
        ),
    ]
