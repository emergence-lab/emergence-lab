# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_datafile_forward(apps, schema_editor):
    DataFile = apps.get_model('core', 'DataFile')
    for f in DataFile.objects.all():
        f.process = f.processes.first()
        f.save()


def migrate_datafile_backward(apps, schema_editor):
    DataFile = apps.get_model('core', 'DataFile')
    for f in DataFile.objects.all():
        f.processes.add(f.process)
        f.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150424_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='process',
            field=models.ForeignKey(related_query_name='datafiles', related_name='datafiles', default=None, null=True, to='core.Process'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_datafile_forward, migrate_datafile_backward),
    ]
