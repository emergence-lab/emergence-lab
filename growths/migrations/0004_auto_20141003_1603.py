# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0003_move_platter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growth',
            name='investigation',
            field=models.ForeignKey(to='core.Investigation'),
        ),
        migrations.AlterField(
            model_name='growth',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
    ]
