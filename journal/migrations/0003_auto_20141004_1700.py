# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20141003_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal_entry',
            name='investigations',
            field=models.ManyToManyField(to=b'core.Investigation'),
        ),
    ]
