# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 6, 20, 37, 56, 310491, tzinfo=utc), verbose_name='date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 6, 20, 38, 2, 768996, tzinfo=utc), verbose_name='date modified', auto_now=True),
            preserve_default=False,
        ),
    ]
