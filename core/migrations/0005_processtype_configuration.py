# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 19:51
from __future__ import unicode_literals

import core.configuration.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_core_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtype',
            name='configuration',
            field=core.configuration.fields.ConfigurationField(default=core.configuration.fields.ConfigurationDict),
        ),
    ]
