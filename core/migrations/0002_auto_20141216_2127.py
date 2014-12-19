# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processnode',
            name='process',
            field=models.ForeignKey(to='core.Process', null=True),
            preserve_default=True,
        ),
    ]
