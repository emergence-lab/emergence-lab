# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_processnode_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessType',
            fields=[
                ('slug', models.SlugField(default='generic-process', max_length=100, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='process',
            name='type',
            field=models.ForeignKey(to='core.ProcessType', null=True),
            preserve_default=True,
        ),
    ]
