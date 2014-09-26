# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='investigation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('active', models.BooleanField(default=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'investigations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'operators',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='platter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('active', models.BooleanField(default=True)),
                ('serial', models.CharField(max_length=20, blank=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'platters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('active', models.BooleanField(default=True)),
                ('core', models.BooleanField(default=False)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='project_tracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_pi', models.BooleanField(default=False)),
                ('operator', models.ForeignKey(to='core.operator')),
                ('project', models.ForeignKey(to='core.project')),
            ],
            options={
                'db_table': 'project_operator_tracking',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='operator',
            name='projects',
            field=models.ManyToManyField(to='core.project', through='core.project_tracking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operator',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(to='core.project'),
            preserve_default=True,
        ),
    ]
