# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HallData',
            fields=[
                ('datafile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.DataFile')),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, default=300.0, max_digits=7)),
                ('symmetry_factor', models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=7)),
                ('sheet_coefficient', models.FloatField(blank=True, null=True)),
                ('sheet_resistance', models.FloatField(blank=True, null=True)),
                ('sheet_concentration', models.FloatField(blank=True, null=True)),
                ('thickness', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('mobility', models.FloatField(blank=True, null=True)),
                ('bulk_coefficient', models.FloatField(blank=True, null=True)),
                ('bulk_resistance', models.FloatField(blank=True, null=True)),
                ('bulk_concentration', models.FloatField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.datafile',),
        ),
    ]
