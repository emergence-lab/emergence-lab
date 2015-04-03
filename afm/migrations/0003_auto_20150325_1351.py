# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afm', '0002_afmfile_image_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afmfile',
            name='image_type',
            field=models.CharField(default='Height', max_length=45, choices=[('Height', 'Height'), ('Amplitude', 'Amplitude'), ('Phase', 'Phase')]),
            preserve_default=True,
        ),
    ]
