# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150416_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='content_type',
            field=models.CharField(default='', max_length=200, blank=True, choices=[('', 'Unknown'), ('application/octet-stream', 'Binary File'), ('application/pdf', 'PDF File'), ('application/vnd.ms-excel', 'Excel File'), ('application/vnd.openxmlformats-officedocument.spreadsheelml.sheet', 'Excel File'), ('image/png', 'PNG Image'), ('image/bmp', 'BMP Image'), ('image/jpeg', 'JPEG Image'), ('image/tiff', 'TIFF Image'), ('image/gif', 'GIF Image'), ('text/plain', 'Plaintext File'), ('text/csv', 'CSV File')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='processes',
            field=models.ManyToManyField(related_query_name='datafiles_old', related_name='datafiles_old', to='core.Process'),
            preserve_default=True,
        ),
    ]
