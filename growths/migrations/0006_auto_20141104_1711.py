# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0005_auto_20141004_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growth',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
    ]
