# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sem.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SEMScan',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
                ('image_number', models.IntegerField(default=0)),
                ('image', models.ImageField(max_length=150, null=True, upload_to=sem.models.get_file_path, blank=True)),
                ('magnification', models.FloatField(null=True, blank=True)),
                ('image_source', models.CharField(default='esem_600', max_length=45, choices=[('leo1550', 'LEO 1550'), ('esem_600', 'FEI sSEM'), ('fib_1200', 'FEI Dual-Beam FIB')])),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
    ]
