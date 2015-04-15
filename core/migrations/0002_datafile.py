# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.process


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.CharField(max_length=10, null=True, blank=True)),
                ('data', models.FileField(max_length=200, null=True, upload_to=core.models.process.get_file_path, blank=True)),
                ('process', models.ManyToManyField(to='core.Process')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
