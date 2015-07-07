# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressupdate',
            name='milestone',
            field=models.ManyToManyField(related_query_name='progress', related_name='progress', to='project_management.Milestone'),
            preserve_default=True,
        ),
    ]
