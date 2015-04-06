# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_growth_number(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        process.legacy_identifier = process.growth_number
        process.save()


def migrate_legacy_identifier(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        process.growth_number = process.legacy_identifier
        process.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150406_0946'),
        ('d180', '0004_d180growth_growth_number'),
    ]

    operations = [
        migrations.RunPython(migrate_growth_number, migrate_legacy_identifier)
    ]
