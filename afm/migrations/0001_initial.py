# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import afm.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AFMScan',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
                ('scan_number', models.IntegerField(default=0)),
                ('rms', models.DecimalField(max_digits=7, decimal_places=3)),
                ('zrange', models.DecimalField(max_digits=7, decimal_places=3)),
                ('location', models.CharField(default='c', max_length=45, choices=[('c', 'Center'), ('r', 'Round'), ('f', 'Flat')])),
                ('size', models.DecimalField(max_digits=7, decimal_places=3)),
                ('height', models.ImageField(max_length=150, null=True, upload_to=afm.models.get_afm_path, blank=True)),
                ('amplitude', models.ImageField(max_length=150, null=True, upload_to=afm.models.get_afm_path, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
    ]
