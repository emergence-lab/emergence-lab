# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_delete_platter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='projects',
            field=models.ManyToManyField(to=b'core.Project', through='core.project_tracking'),
        ),
        migrations.AlterField(
            model_name='project_tracking',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
        migrations.AlterField(
            model_name='projecttracking',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
        migrations.AlterField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(related_query_name='user', related_name='users', to=b'core.Project', through='core.ProjectTracking', blank=True, help_text='Projects this user is tracking', verbose_name='tracked projects'),
        ),
    ]
