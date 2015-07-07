# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0004_auto_20150601_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressupdate',
            name='datafile',
        ),
        migrations.RemoveField(
            model_name='progressupdate',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='progressupdate',
            name='process',
        ),
        migrations.DeleteModel(
            name='ProgressUpdate',
        ),
        migrations.AddField(
            model_name='milestone',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
