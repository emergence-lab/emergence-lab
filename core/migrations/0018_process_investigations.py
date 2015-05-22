# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_investigations_forward(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        for investigation in process.investigations_old.all():
            process.investigations.add(investigation)


def migrate_investigations_backward(apps, schema_editor):
    D180Process = apps.get_model('d180', 'D180Growth')
    for process in D180Process.objects.all():
        for investigation in process.investigations.all():
            process.investigations_old.add(investigation)



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20150521_1736'),
        ('d180', '0011_rename_investigations'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='investigations',
            field=models.ManyToManyField(related_query_name='process', related_name='processes', to='core.Investigation'),
            preserve_default=True,
        ),
        migrations.RunPython(migrate_investigations_forward, migrate_investigations_backward),
    ]
