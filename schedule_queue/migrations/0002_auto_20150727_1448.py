# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0001_initial'),
        ('core', '0017_remove_splitprocess'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='bake_length_in_minutes',
            new_name='bake_length',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='growth_length_in_hours',
            new_name='growth_length',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='priority_field',
            new_name='priority',
        ),
        migrations.AddField(
            model_name='reservation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=utc), verbose_name='date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 0, 0, 0, 0, tzinfo=utc), verbose_name='date modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='tool',
            field=models.ForeignKey(related_query_name='reservation', related_name='reservations', to='core.ProcessType'),
            preserve_default=True,
        ),
    ]
