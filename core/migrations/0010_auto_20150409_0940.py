# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150406_1213'),
        ('d180', '0006_auto_20150409_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafile',
            name='content_type',
            field=models.CharField(default='', max_length=45, blank=True, choices=[('', 'Unknown'), ('application/octet-stream', 'Binary File'), ('application/pdf', 'PDF File'), ('application/vnd.ms-excel', 'Excel File'), ('application/vnd.openxmlformats-officedocument.spreadsheelml.sheet', 'Excel File'), ('image/png', 'PNG Image'), ('image/bmp', 'BMP Image'), ('image/jpeg', 'JPEG Image'), ('image/tiff', 'TIFF Image'), ('image/gif', 'GIF Image'), ('text/plain', 'Plaintext File')]),
            preserve_default=True,
        ),
    ]
