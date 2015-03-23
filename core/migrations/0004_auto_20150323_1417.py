# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150311_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 23, 18, 17, 32, 549451, tzinfo=utc), verbose_name='date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datafile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 23, 18, 17, 39, 901548, tzinfo=utc), verbose_name='date modified', auto_now=True),
            preserve_default=False,
        ),
    ]
