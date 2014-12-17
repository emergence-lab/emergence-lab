# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20141215_1155'),
        ('simulations', '0002_auto_20141215_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='command',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='elapsed_time',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='input_file_path',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='output_file_path',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='runfile',
        ),
        migrations.AddField(
            model_name='simulation',
            name='investigations',
            field=models.ManyToManyField(to='core.Investigation'),
            preserve_default=True,
        ),
    ]
