# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_processtype_creation_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', verbose_name='slug', editable=False),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', verbose_name='slug', editable=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', verbose_name='slug', editable=False),
        ),
    ]
