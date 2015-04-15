# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150311_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='SEMScan',
            fields=[
                ('process_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Process')),
                ('image_source', models.CharField(default='esem_600', max_length=45, null=True, blank=True, choices=[('leo1550', 'LEO 1550'), ('esem_600', 'FEI eSEM'), ('fib_1200', 'FEI Dual-Beam FIB')])),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
    ]
