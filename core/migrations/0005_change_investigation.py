# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20140929_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investigation',
            options={'verbose_name': 'investigation', 'verbose_name_plural': 'investigations'},
        ),
        migrations.AlterField(
            model_name='investigation',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='name',
            field=models.CharField(max_length=45, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='slug',
            field=autoslug.fields.AutoSlugField(verbose_name='slug', editable=False),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date started'),
        ),
    ]
