# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_user_forward(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        process.user = process.user_old
        process.save()


def migrate_user_backward(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        process.user_old = process.user
        process.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150409_0940'),
        ('d180', '0006_auto_20150409_0938'),
    ]

    operations = [
        migrations.RunPython(migrate_user_forward, migrate_user_backward)
    ]
