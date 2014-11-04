# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20141004_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='core.Project'),
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
    ]
