# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('title', models.CharField(max_length=100)),
                ('entry', core.models.fields.RichTextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('investigations', models.ManyToManyField(to='core.Investigation')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='journal_entry',
            name='author',
        ),
        migrations.RemoveField(
            model_name='journal_entry',
            name='investigations',
        ),
        migrations.DeleteModel(
            name='journal_entry',
        ),
    ]
