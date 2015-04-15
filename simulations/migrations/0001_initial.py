# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import simulations.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('finish_date', models.DateTimeField(null=True, blank=True)),
                ('file_path', models.FileField(help_text=b'ZIP File with all simulation data', storage=simulations.models.FixedS3BotoStorage(querystring_expire=600, querystring_auth=True, acl=b'private'), null=True, upload_to=simulations.models.content_file_name, blank=True)),
                ('priority', models.BooleanField(default=False)),
                ('execution_node', models.CharField(max_length=15, choices=[('t2.micro', b'micro (t2)')])),
                ('investigations', models.ManyToManyField(to='core.Investigation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
