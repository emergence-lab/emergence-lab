# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import pytz

from django.db import models, migrations


def migrate_end_date_data(apps, schema_editor):
    Platter = apps.get_model('core', 'platter')
    for platter in Platter.objects.all():
        if platter.end_date is not None:
            dt = datetime.datetime(platter.end_date.year,
                     platter.end_date.month, platter.end_date.day)
            platter.status_changed = pytz.utc.localize(dt)
            platter.save()


def reverse_migrate_end_date_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_add_status_changed_activestatemixin'),
    ]

    operations = [
        migrations.RunPython(migrate_end_date_data, reverse_migrate_end_date_data),
    ]
