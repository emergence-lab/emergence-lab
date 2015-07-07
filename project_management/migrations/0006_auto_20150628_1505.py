# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0005_auto_20150602_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='milestone',
            options={'verbose_name': 'milestone', 'verbose_name_plural': 'milestones'},
        ),
        migrations.AddField(
            model_name='literature',
            name='external_link',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
