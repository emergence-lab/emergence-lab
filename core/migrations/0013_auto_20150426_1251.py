# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150416_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('name', models.CharField(max_length=50, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('process', models.ForeignKey(related_query_name='process', related_name='process', to='core.Process')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='datafile',
            name='processes',
        ),
        migrations.AddField(
            model_name='datafile',
            name='process',
            field=models.ForeignKey(related_query_name='datafiles', related_name='datafiles', to='core.Process', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='content_type',
            field=models.CharField(default='', max_length=200, blank=True, choices=[('', 'Unknown'), ('application/octet-stream', 'Binary File'), ('application/pdf', 'PDF File'), ('application/vnd.ms-excel', 'Excel File'), ('application/vnd.openxmlformats-officedocument.spreadsheelml.sheet', 'Excel File'), ('image/png', 'PNG Image'), ('image/bmp', 'BMP Image'), ('image/jpeg', 'JPEG Image'), ('image/tiff', 'TIFF Image'), ('image/gif', 'GIF Image'), ('text/plain', 'Plaintext File'), ('text/csv', 'CSV File')]),
            preserve_default=True,
        ),
    ]
