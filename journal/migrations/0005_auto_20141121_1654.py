# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_auto_20141104_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal_entry',
            name='investigations',
            field=models.ManyToManyField(to='core.Investigation'),
            preserve_default=True,
        ),
    ]
