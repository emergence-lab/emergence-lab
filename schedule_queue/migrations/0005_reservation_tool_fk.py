# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_tool_forward(apps, schema_editor):
    Reservation = apps.get_model('schedule_queue', 'Reservation')
    for reservation in Reservation.objects.all():
        reservation.tool_fk_id = reservation.tool
        reservation.save()


def migrate_tool_backward(apps, schema_editor):
    Reservation = apps.get_model('schedule_queue', 'Reservation')
    for reservation in Reservation.objects.all():
        reservation.tool = reservation.tool_fk_id
        reservation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_splitprocess'),
        ('schedule_queue', '0004_longer_tool_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='tool_fk',
            field=models.ForeignKey(default='generic-process', to='core.ProcessType'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_tool_forward, migrate_tool_backward),
    ]
