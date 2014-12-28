# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0007_auto_20141120_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growth',
            name='project',
            field=models.ForeignKey(to='core.Project'),
            preserve_default=True,
        ),
    ]
