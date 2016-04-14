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
            name='AFMFile',
            fields=[
                ('datafile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.DataFile')),
                ('scan_number', models.IntegerField(default=0)),
                ('rms', models.DecimalField(decimal_places=3, max_digits=7)),
                ('zrange', models.DecimalField(decimal_places=3, max_digits=7)),
                ('location', models.CharField(choices=[('c', 'Center'), ('r', 'Round'), ('f', 'Flat')], default='c', max_length=45)),
                ('image_type', models.CharField(choices=[('Raw', 'Raw'), ('Height', 'Height'), ('Amplitude', 'Amplitude'), ('Phase', 'Phase')], default='Height', max_length=45)),
                ('size', models.DecimalField(decimal_places=3, max_digits=7)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.datafile',),
        ),
    ]
