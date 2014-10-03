# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal_entry',
            name='investigations',
            field=models.ManyToManyField(to=b'core.Investigation'),
        ),
    ]
