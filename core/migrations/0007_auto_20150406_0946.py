# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150325_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='legacy_identifier',
            field=models.SlugField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investigation',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', verbose_name='slug', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', verbose_name='slug', editable=False),
            preserve_default=True,
        ),
    ]
