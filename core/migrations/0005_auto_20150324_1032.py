# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('core', '0004_auto_20150323_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_core.datafile_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafile',
            name='state',
            field=models.CharField(default='raw', max_length=20, choices=[('raw', 'Raw'), ('cleaned', 'Cleaned'), ('extracted', 'Extracted'), ('analyzed', 'Analyzed'), ('other', 'Other')]),
            preserve_default=True,
        ),
    ]
