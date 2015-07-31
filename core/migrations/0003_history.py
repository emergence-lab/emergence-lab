# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_processtypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProcess',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created', models.DateTimeField(verbose_name='date created', editable=False, blank=True)),
                ('modified', models.DateTimeField(verbose_name='date modified', editable=False, blank=True)),
                ('uuid_full', core.models.fields.UUIDField(db_index=True, max_length=32, editable=False, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('legacy_identifier', models.SlugField(max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('type', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.ProcessType', null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical process',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSample',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created', models.DateTimeField(verbose_name='date created', editable=False, blank=True)),
                ('modified', models.DateTimeField(verbose_name='date modified', editable=False, blank=True)),
                ('comment', core.models.fields.RichTextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('process_tree', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.ProcessNode', null=True)),
                ('substrate', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Substrate', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical sample',
            },
            bases=(models.Model,),
        ),
    ]
