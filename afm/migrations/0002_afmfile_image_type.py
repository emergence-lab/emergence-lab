# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='afmfile',
            name='image_type',
            field=models.CharField(default='height', max_length=45, choices=[('height', 'Height'), ('amplitude', 'Amplitude'), ('phase', 'Phase')]),
            preserve_default=True,
        ),
    ]
