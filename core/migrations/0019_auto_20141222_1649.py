# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20141215_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='core.Project'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project_tracking',
            name='project',
            field=models.ForeignKey(to='core.Project'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttracking',
            name='project',
            field=models.ForeignKey(to='core.Project'),
            preserve_default=True,
        ),
    ]
