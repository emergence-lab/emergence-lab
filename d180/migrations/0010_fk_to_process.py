# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0009_rename_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d180readings',
            name='description',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='d180readings',
            name='process',
            field=models.ForeignKey(related_name='readings', to='core.Process'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='d180recipelayer',
            name='process',
            field=models.ForeignKey(related_name='recipe', to='core.Process'),
            preserve_default=True,
        ),
    ]
