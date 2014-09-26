# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='journal_entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('entry', ckeditor.fields.RichTextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('author', models.ForeignKey(to='core.operator')),
                ('investigations', models.ManyToManyField(to='core.investigation')),
            ],
            options={
                'db_table': 'journal_entries',
            },
            bases=(models.Model,),
        ),
    ]
