# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_project_tracking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operator',
            options={'verbose_name': 'operator', 'verbose_name_plural': 'operators'},
        ),
        migrations.AlterModelOptions(
            name='platter',
            options={'verbose_name': 'platter', 'verbose_name_plural': 'platters'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
        migrations.AlterField(
            model_name='operator',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='platter',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='platter',
            name='end_date',
            field=models.DateField(null=True, verbose_name='date retired', blank=True),
        ),
        migrations.AlterField(
            model_name='platter',
            name='name',
            field=models.CharField(max_length=45, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='platter',
            name='serial',
            field=models.CharField(max_length=20, verbose_name='serial number', blank=True),
        ),
        migrations.AlterField(
            model_name='platter',
            name='start_date',
            field=models.DateField(auto_now_add=True, verbose_name='date started'),
        ),
        migrations.AlterField(
            model_name='project',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='project',
            name='core',
            field=models.BooleanField(default=False, verbose_name='core project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=45, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(verbose_name='slug', editable=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date started'),
        ),
    ]
