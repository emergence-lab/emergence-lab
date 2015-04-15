# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('investigations', models.ManyToManyField(to='core.Investigation')),
            ],
            options={
                'db_table': 'journal_entries',
            },
            bases=(models.Model,),
        ),
    ]
