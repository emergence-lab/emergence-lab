# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_datafile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='process',
        ),
        migrations.AddField(
            model_name='datafile',
            name='processes',
            field=models.ManyToManyField(related_query_name='datafiles', related_name='datafiles', to='core.Process'),
            preserve_default=True,
        ),
    ]
