# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150324_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='AFMFile',
            fields=[
                ('datafile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.DataFile')),
                ('scan_number', models.IntegerField(default=0)),
                ('rms', models.DecimalField(max_digits=7, decimal_places=3)),
                ('zrange', models.DecimalField(max_digits=7, decimal_places=3)),
                ('location', models.CharField(default='c', max_length=45, choices=[('c', 'Center'), ('r', 'Round'), ('f', 'Flat')])),
                ('size', models.DecimalField(max_digits=7, decimal_places=3)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.datafile',),
        ),
        migrations.CreateModel(
            name='AFMScan',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
    ]
