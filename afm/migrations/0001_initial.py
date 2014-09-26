# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import afm.models


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='afm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scan_number', models.IntegerField(default=0)),
                ('rms', models.DecimalField(max_digits=7, decimal_places=3)),
                ('zrange', models.DecimalField(max_digits=7, decimal_places=3)),
                ('location', models.CharField(default=b'c', max_length=45, choices=[(b'c', b'Center'), (b'r', b'Round'), (b'f', b'Flat')])),
                ('size', models.DecimalField(max_digits=7, decimal_places=3)),
                ('height', models.ImageField(max_length=150, null=True, upload_to=afm.models.get_afm_path, blank=True)),
                ('amplitude', models.ImageField(max_length=150, null=True, upload_to=afm.models.get_afm_path, blank=True)),
                ('growth', models.ForeignKey(to='growths.growth')),
                ('sample', models.ForeignKey(to='growths.sample')),
            ],
            options={
                'db_table': 'afm',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='afm',
            unique_together=set([('growth', 'sample', 'scan_number', 'location')]),
        ),
    ]
