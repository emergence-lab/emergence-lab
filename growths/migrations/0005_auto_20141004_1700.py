# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0004_auto_20141003_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growth',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
    ]
