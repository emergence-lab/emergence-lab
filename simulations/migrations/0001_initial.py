# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('finish_date', models.DateTimeField(null=True, blank=True)),
                ('elapsed_time', models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True)),
                ('priority', models.BooleanField(default=False)),
                ('execution_node', models.CharField(max_length=15, choices=[('t2.micro', b'micro (t2)')])),
                ('completed', models.BooleanField(default=False)),
                ('input_file_path', models.CharField(max_length=500, blank=True)),
                ('output_file_path', models.CharField(max_length=500, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
